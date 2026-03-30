from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db, Session, Response

sessions_bp = Blueprint('sessions', __name__)


@sessions_bp.route('/start', methods=['POST'])
@jwt_required()
def start_session():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    job_role = data.get('job_role', 'General')
    level = data.get('level', 'beginner')

    session = Session(user_id=user_id, job_role=job_role, level=level)
    db.session.add(session)
    db.session.commit()
    return jsonify({'session_id': session.id}), 201


@sessions_bp.route('/', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = int(get_jwt_identity())
    sessions = Session.query.filter_by(user_id=user_id).order_by(Session.started_at.desc()).all()
    result = []
    for s in sessions:
        s_dict = s.to_dict()
        s_dict['responses'] = [r.to_dict() for r in s.responses]
        result.append(s_dict)
    return jsonify(result), 200


@sessions_bp.route('/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    user_id = int(get_jwt_identity())
    session = Session.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    s_dict = session.to_dict()
    s_dict['responses'] = [r.to_dict() for r in session.responses]
    return jsonify(s_dict), 200


@sessions_bp.route('/<int:session_id>/complete', methods=['POST'])
@jwt_required()
def complete_session(session_id):
    user_id = int(get_jwt_identity())
    session = Session.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    session.completed_at = datetime.utcnow()
    scores = [r.overall_score for r in session.responses if r.overall_score is not None]
    session.overall_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    db.session.commit()
    return jsonify(session.to_dict()), 200
