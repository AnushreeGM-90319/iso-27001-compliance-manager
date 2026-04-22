from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import call_groq

describe_bp = Blueprint('describe', __name__)

@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.json

    # Validate input
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_input = data['text']

    # Load prompt template
    try:
        with open("prompts/describe_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()
    except:
        return jsonify({"error": "Prompt file not found"}), 500

    prompt = template.replace("{input}", user_input)

    # Call AI
    ai_response = call_groq(prompt)

    return jsonify({
        "description": ai_response,
        "generated_at": datetime.utcnow().isoformat()
    })