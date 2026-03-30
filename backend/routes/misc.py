from flask import Blueprint, request, jsonify

misc_bp = Blueprint('misc', __name__)


@misc_bp.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    email = data.get('email', '')
    message = data.get('message', '')
    if not email or not message:
        return jsonify({'error': 'Email and message are required'}), 400
    # In production, send via email service
    print(f'Contact form: {email} — {message}')
    return jsonify({'message': 'Message received. We will get back to you soon!'}), 200


@misc_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200
