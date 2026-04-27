from flask import Flask, request, jsonify
from services.groq_client import get_groq_response

app = Flask(__name__)
@app.route('/')
def home():
    return "API is running!"
@app.route('/describe', methods=['POST'])
@app.route('/test')
def test():
    user_input = "Explain AI in simple words"
    response = get_groq_response(user_input)
    return response
def describe():
    try:
        data = request.get_json()

        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        
        if 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        user_input = data['text']

       
        if user_input.strip() == "":
            return jsonify({"error": "Text cannot be empty"}), 400

        
        response = get_groq_response(user_input)

        return jsonify({
            "status": "success",
            "response": response
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)