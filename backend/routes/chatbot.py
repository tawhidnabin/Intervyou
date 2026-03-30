from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.chatbot import InterviewCoach

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message to the AI coach and get a response."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    history = data.get('history', [])

    if not message:
        return jsonify({'error': 'Message is required.'}), 400

    context = InterviewCoach.build_context(history)
    response = InterviewCoach.chat(message, context)

    return jsonify({'response': response}), 200


@chatbot_bp.route('/session-feedback', methods=['POST'])
@jwt_required()
def session_feedback():
    """Generate AI coaching feedback for a completed session."""
    data = request.get_json() or {}
    job_role = data.get('job_role', 'General')
    level = data.get('level', 'beginner')
    overall_score = data.get('overall_score', 0)
    question_results = data.get('question_results', [])

    feedback = InterviewCoach.generate_session_feedback(
        job_role, level, overall_score, question_results
    )

    return jsonify({'feedback': feedback}), 200
