import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, Question, TokenBlocklist


def seed_questions(app):
    with app.app_context():
        if Question.query.count() == 0:
            from seed_questions import QUESTIONS
            for text, category, difficulty, ideal_answer in QUESTIONS:
                db.session.add(Question(
                    text=text, category=category,
                    difficulty=difficulty, ideal_answer=ideal_answer
                ))
            db.session.commit()
            print(f'Seeded {len(QUESTIONS)} questions across all categories and levels.')


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///intervyou.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY', 'intervyou-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

    db.init_app(app)
    jwt = JWTManager(app)

    # CORS: allow localhost for dev + Vercel domain for production
    allowed_origins = [
        'http://localhost:4200',
        os.environ.get('FRONTEND_URL', 'http://localhost:4200')
    ]
    CORS(app, resources={r'/api/*': {'origins': allowed_origins}}, supports_credentials=True)

    # Check if token is revoked (logout support)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    from routes.auth import auth_bp
    from routes.questions import questions_bp
    from routes.sessions import sessions_bp
    from routes.analysis import analysis_bp
    from routes.user import user_bp
    from routes.misc import misc_bp
    from routes.chatbot import chatbot_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(misc_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    with app.app_context():
        db.create_all()
        seed_questions(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
