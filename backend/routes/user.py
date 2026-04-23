import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Session

user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def dashboard_stats():
    user_id = int(get_jwt_identity())
    sessions = Session.query.filter_by(user_id=user_id).all()
    completed = [s for s in sessions if s.overall_score is not None]
    avg_score = round(sum(s.overall_score for s in completed) / len(completed), 1) if completed else 0
    return jsonify({
        'sessions_count': len(sessions),
        'avg_score': avg_score,
        'completed_count': len(completed)
    }), 200


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json() or {}

    if 'name' in data:
        name = data['name'].strip()
        if len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters.'}), 400
        user.name = name

    if 'email' in data:
        new_email = data['email'].lower().strip()
        if new_email != user.email:
            if User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'This email is already in use.'}), 409
            user.email = new_email
            user.email_verified = False  # re-verify on email change

    db.session.commit()
    return jsonify({'user': user.to_dict(), 'message': 'Profile updated.'}), 200


@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json() or {}
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not check_password_hash(user.password_hash, old_password):
        return jsonify({'error': 'Current password is incorrect.'}), 400

    if len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters.'}), 400
    if not re.search(r'[A-Z]', new_password):
        return jsonify({'error': 'New password must contain at least one uppercase letter.'}), 400
    if not re.search(r'[a-z]', new_password):
        return jsonify({'error': 'New password must contain at least one lowercase letter.'}), 400
    if not re.search(r'[0-9]', new_password):
        return jsonify({'error': 'New password must contain at least one number.'}), 400

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully.'}), 200


@user_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    # Delete all user data
    for session in user.sessions:
        for response in session.responses:
            db.session.delete(response)
        db.session.delete(session)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Account deleted.'}), 200
