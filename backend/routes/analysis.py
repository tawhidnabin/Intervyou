import os
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Response, Question
from services.transcription import transcribe
from services.audio_analysis import analyze_audio, analyze_transcript
from services.nlp_analysis import score_relevance
from services.feedback import generate_feedback, compute_overall_score

analysis_bp = Blueprint('analysis', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')


@analysis_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_analysis():
    """Audio submission — Whisper + Librosa + BERT."""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    session_id = request.form.get('session_id')
    question_id = request.form.get('question_id')

    if not session_id or not question_id:
        return jsonify({'error': 'session_id and question_id are required'}), 400

    question = Question.query.get(int(question_id))
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    filename = f'{uuid.uuid4()}.webm'
    audio_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    audio_file.save(audio_path)

    try:
        transcript = transcribe(audio_path)
        audio_metrics = analyze_audio(audio_path)
        text_metrics = analyze_transcript(transcript, audio_metrics['duration_seconds'])
        relevance = score_relevance(transcript, question.ideal_answer)
        feedback = generate_feedback(
            text_metrics['speaking_rate'], text_metrics['filler_count'],
            audio_metrics['pause_count'], relevance, text_metrics['fluency_score']
        )
        overall = compute_overall_score(relevance, text_metrics['fluency_score'])

        response = Response(
            session_id=int(session_id), question_id=int(question_id),
            audio_path=audio_path, transcript=transcript,
            speaking_rate=text_metrics['speaking_rate'],
            filler_count=text_metrics['filler_count'],
            pause_count=audio_metrics['pause_count'],
            relevance_score=relevance, fluency_score=text_metrics['fluency_score'],
            overall_score=overall, feedback_text=feedback
        )
        db.session.add(response)
        db.session.commit()

        return jsonify({
            'response_id': response.id, 'transcript': transcript,
            'speaking_rate': text_metrics['speaking_rate'],
            'filler_count': text_metrics['filler_count'],
            'pause_count': audio_metrics['pause_count'],
            'relevance_score': relevance, 'fluency_score': text_metrics['fluency_score'],
            'overall_score': overall, 'feedback': feedback,
            'input_mode': 'voice'
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Pipeline failed: {str(e)}'}), 500


@analysis_bp.route('/submit-text', methods=['POST'])
@jwt_required()
def submit_text_analysis():
    """Text submission — NLP scoring only."""
    data = request.get_json() or {}
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    answer_text = data.get('answer_text', '').strip()

    if not session_id or not question_id:
        return jsonify({'error': 'session_id and question_id are required'}), 400
    if not answer_text:
        return jsonify({'error': 'Please type your answer before submitting.'}), 400
    if len(answer_text) < 20:
        return jsonify({'error': 'Your answer is too short. Please provide a more detailed response.'}), 400

    question = Question.query.get(int(question_id))
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    try:
        words = answer_text.split()
        word_count = len(words)
        estimated_duration = max(word_count / 2.0, 1.0)
        text_metrics = analyze_transcript(answer_text, estimated_duration)
        relevance = score_relevance(answer_text, question.ideal_answer)
        fluency = text_metrics['fluency_score']
        feedback = generate_feedback(
            text_metrics['speaking_rate'], text_metrics['filler_count'],
            0, relevance, fluency
        )
        overall = compute_overall_score(relevance, fluency)

        response = Response(
            session_id=int(session_id), question_id=int(question_id),
            audio_path=None, transcript=answer_text,
            speaking_rate=text_metrics['speaking_rate'],
            filler_count=text_metrics['filler_count'],
            pause_count=0, relevance_score=relevance,
            fluency_score=fluency, overall_score=overall,
            feedback_text=feedback
        )
        db.session.add(response)
        db.session.commit()

        return jsonify({
            'response_id': response.id, 'transcript': answer_text,
            'speaking_rate': text_metrics['speaking_rate'],
            'filler_count': text_metrics['filler_count'],
            'pause_count': 0,
            'relevance_score': relevance, 'fluency_score': fluency,
            'overall_score': overall, 'feedback': feedback,
            'input_mode': 'text'
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@analysis_bp.route('/ai-feedback/<int:response_id>', methods=['POST'])
@jwt_required()
def generate_ai_feedback(response_id):
    """Generate LLM analytical feedback on demand (called by frontend after scores load)."""
    response = Response.query.get(response_id)
    if not response:
        return jsonify({'error': 'Response not found'}), 404

    # If already generated, return cached
    if response.ai_analysis:
        return jsonify({'ai_analysis': response.ai_analysis, 'ready': True}), 200

    # Generate now
    try:
        from services.chatbot import InterviewCoach
        question_text = response.question.text if response.question else ''
        metrics = {
            'overall_score': response.overall_score or 0,
            'relevance_score': response.relevance_score or 0,
            'fluency_score': response.fluency_score or 0,
            'speaking_rate': response.speaking_rate or 0,
            'filler_count': response.filler_count or 0,
            'pause_count': response.pause_count or 0
        }
        input_mode = 'text' if not response.audio_path else 'voice'

        ai_feedback = InterviewCoach.analyze_response(
            question_text, response.transcript or '', metrics, input_mode
        )

        if ai_feedback:
            response.ai_analysis = ai_feedback
            db.session.commit()
            return jsonify({'ai_analysis': ai_feedback, 'ready': True}), 200
        else:
            return jsonify({'ai_analysis': None, 'ready': False, 'error': 'LLM returned empty response'}), 200

    except Exception as e:
        print(f'AI feedback generation error: {e}')
        return jsonify({
            'ai_analysis': None, 'ready': False,
            'error': 'Could not connect to Ollama. Make sure it is running.'
        }), 200
