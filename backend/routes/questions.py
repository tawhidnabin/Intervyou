from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import Question
import random

questions_bp = Blueprint('questions', __name__)

# Map level names to difficulty values
LEVEL_MAP = {
    'beginner': 'easy',
    'intermediate': 'medium',
    'master': 'hard'
}


@questions_bp.route('/', methods=['GET'])
@jwt_required()
def get_questions():
    level = request.args.get('level', 'beginner')
    difficulty = LEVEL_MAP.get(level, 'easy')

    questions = Question.query.filter_by(difficulty=difficulty).all()

    # Fallback: if not enough questions for this difficulty, include all
    if len(questions) < 3:
        questions = Question.query.all()

    # Shuffle and return up to 5
    random.shuffle(questions)
    return jsonify([q.to_dict() for q in questions[:5]]), 200
