import re
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, TokenBlocklist

auth_bp = Blueprint('auth', __name__)

# ── Validation helpers ───────────────────────────────────────────────

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PASSWORD_MIN = 8


def validate_email(email: str) -> str | None:
    if not email:
        return 'Email is required.'
    if not EMAIL_RE.match(email):
        return 'Please enter a valid email address.'
    return None


def validate_password(password: str) -> str | None:
    if not password or len(password) < PASSWORD_MIN:
        return f'Password must be at least {PASSWORD_MIN} characters.'
    if not re.search(r'[A-Z]', password):
        return 'Password must contain at least one uppercase letter.'
    if not re.search(r'[a-z]', password):
        return 'Password must contain at least one lowercase letter.'
    if not re.search(r'[0-9]', password):
        return 'Password must contain at least one number.'
    return None


def validate_name(name: str) -> str | None:
    if not name or len(name.strip()) < 2:
        return 'Name must be at least 2 characters.'
    if len(name.strip()) > 100:
        return 'Name must be under 100 characters.'
    return None


# ── Register ─────────────────────────────────────────────────────────

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email', '').lower().strip()
    password = data.get('password', '')
    name = data.get('name', '').strip()

    # Validate all fields
    err = validate_name(name)
    if err:
        return jsonify({'error': err}), 400
    err = validate_email(email)
    if err:
        return jsonify({'error': err}), 400
    err = validate_password(password)
    if err:
        return jsonify({'error': err}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists.'}), 409

    verification_token = secrets.token_urlsafe(32)

    user = User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password),
        email_verified=False,
        verification_token=verification_token
    )
    db.session.add(user)
    db.session.commit()

    # In production: send verification email here
    # For dev: auto-log in and return the verification token for testing
    access_token = create_access_token(identity=str(user.id), fresh=True)
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(),
        'message': 'Account created. Please verify your email.',
        'verification_token': verification_token  # remove in production
    }), 201


# ── Login ────────────────────────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').lower().strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    access_token = create_access_token(identity=str(user.id), fresh=True)
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


# ── Refresh token ────────────────────────────────────────────────────

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify({'token': access_token}), 200


# ── Logout (revoke token) ───────────────────────────────────────────

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({'message': 'Successfully logged out.'}), 200


# ── Get current user ────────────────────────────────────────────────

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify(user.to_dict()), 200


# ── Verify email ────────────────────────────────────────────────────

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json() or {}
    token = data.get('token', '')

    if not token:
        return jsonify({'error': 'Verification token is required.'}), 400

    user = User.query.filter_by(verification_token=token).first()
    if not user:
        return jsonify({'error': 'Invalid or expired verification token.'}), 400

    user.email_verified = True
    user.verification_token = None
    db.session.commit()

    return jsonify({'message': 'Email verified successfully.', 'user': user.to_dict()}), 200


# ── Resend verification email ───────────────────────────────────────

@auth_bp.route('/resend-verification', methods=['POST'])
@jwt_required()
def resend_verification():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    if user.email_verified:
        return jsonify({'message': 'Email is already verified.'}), 200

    user.verification_token = secrets.token_urlsafe(32)
    db.session.commit()

    # In production: send email here
    return jsonify({
        'message': 'Verification email sent.',
        'verification_token': user.verification_token  # remove in production
    }), 200


# ── Forgot password ─────────────────────────────────────────────────

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email', '').lower().strip()

    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal whether email exists
        return jsonify({'message': 'If an account exists, a reset link has been sent.'}), 200

    user.reset_token = secrets.token_urlsafe(32)
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    # In production: send reset email here
    return jsonify({
        'message': 'If an account exists, a reset link has been sent.',
        'reset_token': user.reset_token  # remove in production
    }), 200


# ── Reset password ──────────────────────────────────────────────────

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    token = data.get('token', '')
    new_password = data.get('new_password', '')

    if not token:
        return jsonify({'error': 'Reset token is required.'}), 400

    err = validate_password(new_password)
    if err:
        return jsonify({'error': err}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user:
        return jsonify({'error': 'Invalid or expired reset token.'}), 400

    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        return jsonify({'error': 'Reset token has expired. Please request a new one.'}), 400

    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.session.commit()

    return jsonify({'message': 'Password reset successfully. You can now sign in.'}), 200
