from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(128), nullable=True)
    reset_token = db.Column(db.String(128), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sessions = db.relationship('Session', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TokenBlocklist(db.Model):
    """Stores revoked JWT tokens for logout."""
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    ideal_answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='medium')
    responses = db.relationship('Response', backref='question', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_role = db.Column(db.String(100))
    level = db.Column(db.String(20), default='beginner')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    responses = db.relationship('Response', backref='session', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_role': self.job_role,
            'level': self.level,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'overall_score': self.overall_score
        }


class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    audio_path = db.Column(db.String(256))
    transcript = db.Column(db.Text)
    speaking_rate = db.Column(db.Float)
    filler_count = db.Column(db.Integer)
    pause_count = db.Column(db.Integer)
    relevance_score = db.Column(db.Float)
    fluency_score = db.Column(db.Float)
    overall_score = db.Column(db.Float)
    feedback_text = db.Column(db.Text)
    ai_analysis = db.Column(db.Text)  # LLM-generated deep analytical feedback
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'question_id': self.question_id,
            'question_text': self.question.text if self.question else None,
            'audio_path': self.audio_path,
            'transcript': self.transcript,
            'speaking_rate': self.speaking_rate,
            'filler_count': self.filler_count,
            'pause_count': self.pause_count,
            'relevance_score': self.relevance_score,
            'fluency_score': self.fluency_score,
            'overall_score': self.overall_score,
            'feedback_text': self.feedback_text,
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
