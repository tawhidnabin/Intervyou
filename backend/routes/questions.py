from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import Question
import random

questions_bp = Blueprint('questions', __name__)

LEVEL_MAP = {
    'beginner': 'easy',
    'intermediate': 'medium',
    'master': 'hard'
}


@questions_bp.route('/', methods=['GET'])
@jwt_required()
def get_questions():
    level = request.args.get('level', 'beginner')
    category = request.args.get('category', 'all')
    count = min(int(request.args.get('count', 5)), 15)  # max 15

    difficulty = LEVEL_MAP.get(level, 'easy')

    query = Question.query.filter_by(difficulty=difficulty)
    if category != 'all':
        query = query.filter_by(category=category)

    questions = query.all()

    # Fallback if not enough
    if len(questions) < 3:
        questions = Question.query.filter_by(difficulty=difficulty).all()
    if len(questions) < 3:
        questions = Question.query.all()

    random.shuffle(questions)
    return jsonify([q.to_dict() for q in questions[:count]]), 200


@questions_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Return available categories with question counts per level."""
    categories = {}
    for q in Question.query.all():
        cat = q.category
        if cat not in categories:
            categories[cat] = {'easy': 0, 'medium': 0, 'hard': 0}
        categories[cat][q.difficulty] = categories[cat].get(q.difficulty, 0) + 1
    return jsonify(categories), 200
