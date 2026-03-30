import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, Question, TokenBlocklist


def seed_questions(app):
    with app.app_context():
        if Question.query.count() == 0:
            questions = [
                # ── BEGINNER (easy) ──────────────────────────────────────────
                Question(text='Tell me about yourself.', category='general', difficulty='easy',
                    ideal_answer='I am a motivated professional with experience in my field. I have developed strong skills through education and practical work. I am passionate about continuous learning and contributing to team success.'),
                Question(text='What are your greatest strengths?', category='general', difficulty='easy',
                    ideal_answer='My greatest strengths are problem-solving, communication, and adaptability. I approach challenges methodically and work well in teams. These strengths have helped me deliver results consistently.'),
                Question(text='Why do you want this job?', category='motivational', difficulty='easy',
                    ideal_answer='I am excited about this role because it aligns with my skills and career goals. The company\'s mission resonates with me and I believe I can make a meaningful contribution while growing professionally.'),
                Question(text='Where do you see yourself in 5 years?', category='motivational', difficulty='easy',
                    ideal_answer='In five years I see myself having grown within this organisation, taking on greater responsibilities. I aim to deepen my expertise and contribute to strategic decisions as a valued team member.'),
                Question(text='What is your biggest weakness?', category='general', difficulty='easy',
                    ideal_answer='I sometimes take on too much work because I want to ensure quality. I have been actively working on delegating tasks and trusting my team, which has improved my productivity and work-life balance.'),
                Question(text='Why should we hire you?', category='general', difficulty='easy',
                    ideal_answer='You should hire me because I bring a combination of relevant skills, enthusiasm, and a strong work ethic. I am a quick learner who adapts well to new environments and I am committed to delivering high-quality results.'),
                Question(text='Tell me about a time you worked in a team.', category='behavioural', difficulty='easy',
                    ideal_answer='In a previous project I collaborated with a cross-functional team to deliver a product launch. I contributed by coordinating communication between departments, ensuring everyone was aligned on goals and deadlines, which led to a successful on-time delivery.'),

                # ── INTERMEDIATE (medium) ────────────────────────────────────
                Question(text='Describe a challenge you overcame.', category='behavioural', difficulty='medium',
                    ideal_answer='I faced a significant challenge when a project deadline was moved forward unexpectedly. I prioritised tasks, communicated clearly with stakeholders, delegated effectively, and worked extra hours to deliver on time. The experience taught me resilience and improved my time management.'),
                Question(text='Tell me about a time you showed leadership.', category='behavioural', difficulty='medium',
                    ideal_answer='When our team lead was absent during a critical sprint, I stepped up to coordinate daily standups, unblock team members, and communicate progress to stakeholders. The sprint was delivered on time and the experience strengthened my leadership confidence.'),
                Question(text='How do you handle conflict with a colleague?', category='behavioural', difficulty='medium',
                    ideal_answer='I address conflict directly but respectfully by first seeking to understand the other person\'s perspective. I arrange a private conversation, listen actively, and focus on finding a solution that works for both parties and the team\'s goals.'),
                Question(text='Describe a time you failed and what you learned.', category='behavioural', difficulty='medium',
                    ideal_answer='I once underestimated the complexity of a feature and missed a deadline. I took ownership, communicated transparently with my manager, created a recovery plan, and delivered within the revised timeline. I learned to break down tasks more carefully and build in buffer time.'),
                Question(text='How do you prioritise when you have multiple deadlines?', category='general', difficulty='medium',
                    ideal_answer='I use a combination of urgency and impact to prioritise. I list all tasks, assess their deadlines and business value, then tackle high-impact urgent items first. I communicate proactively with stakeholders if any deadlines are at risk.'),
                Question(text='Tell me about a time you had to learn something quickly.', category='behavioural', difficulty='medium',
                    ideal_answer='When we adopted a new technology stack mid-project, I dedicated evenings to structured learning, built small prototypes to apply concepts, and paired with more experienced colleagues. Within two weeks I was contributing effectively and later helped onboard others.'),
                Question(text='How do you handle feedback and criticism?', category='general', difficulty='medium',
                    ideal_answer='I welcome feedback as an opportunity to grow. When I receive criticism I listen without becoming defensive, ask clarifying questions to fully understand the concern, and create an action plan to address it. I follow up to show I have acted on the feedback.'),

                # ── MASTER (hard) ────────────────────────────────────────────
                Question(text='Describe a situation where you influenced a decision without direct authority.', category='behavioural', difficulty='hard',
                    ideal_answer='I identified a process inefficiency that was costing the team significant time. Without formal authority, I gathered data to quantify the impact, built a business case, and presented it to senior stakeholders. By aligning the proposal with company OKRs and addressing concerns proactively, I secured buy-in and led the implementation, reducing processing time by 40%.'),
                Question(text='Tell me about the most complex problem you have solved.', category='behavioural', difficulty='hard',
                    ideal_answer='I was tasked with diagnosing a production system degradation affecting thousands of users. I systematically isolated variables, analysed logs and metrics, identified a race condition in a distributed service, and coordinated a hotfix deployment within four hours. I then led a post-mortem and implemented monitoring to prevent recurrence.'),
                Question(text='How do you approach making decisions with incomplete information?', category='general', difficulty='hard',
                    ideal_answer='I identify the minimum viable information needed to make a sound decision, gather it quickly through targeted research and stakeholder input, and assess the risk of being wrong. I make a time-boxed decision, document my reasoning, and build in checkpoints to course-correct as more information emerges.'),
                Question(text='Describe a time you drove significant change in an organisation.', category='behavioural', difficulty='hard',
                    ideal_answer='I championed a shift from waterfall to agile delivery in my department. I started by piloting the approach with one team, measured the improvement in delivery speed and quality, then used those results to build a case for wider adoption. I ran training sessions, addressed resistance through one-on-ones, and the methodology was adopted across three teams within six months.'),
                Question(text='How do you balance technical debt against feature delivery?', category='general', difficulty='hard',
                    ideal_answer='I treat technical debt as a first-class concern by making it visible in the backlog with quantified impact. I advocate for a sustainable ratio — typically 20% of sprint capacity for debt reduction — and frame it in business terms: reduced incident rate, faster feature delivery, lower maintenance cost. I escalate when debt reaches a threshold that threatens delivery velocity.'),
                Question(text='Tell me about a time you had to deliver difficult news to a stakeholder.', category='behavioural', difficulty='hard',
                    ideal_answer='I had to inform a key client that a critical feature would be delayed by three weeks due to an unforeseen technical dependency. I requested an urgent meeting, presented the situation transparently with root cause analysis, offered two mitigation options with trade-offs, and recommended the best path forward. The client appreciated the honesty and we maintained the relationship.'),
                Question(text='How do you build and maintain high-performing teams?', category='general', difficulty='hard',
                    ideal_answer='I focus on psychological safety, clear goals, and individual growth. I establish explicit team norms, run regular one-on-ones to understand motivations and blockers, celebrate wins publicly, and address underperformance privately and constructively. I ensure each person understands how their work connects to the broader mission.'),
            ]
            db.session.add_all(questions)
            db.session.commit()
            print(f'Seeded {len(questions)} questions across all difficulty levels.')


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
