from flask import Flask, request, jsonify, render_template
from services.groq_client import get_groq_response
from datetime import datetime
import json
import logging

app = Flask(__name__)

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO)


# -------------------------------
# HOME ROUTE (UI)
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')  # optional UI


# -------------------------------
# TEST ROUTE (Browser Testing)
# -------------------------------
@app.route('/test')
def test():
    user_input = request.args.get('text')

    if not user_input:
        return "Please provide text using ?text=your_input"

    logging.info(f"Test input: {user_input}")

    response = get_groq_response(user_input)
    return response


# -------------------------------
# DESCRIBE ENDPOINT
# -------------------------------
@app.route('/describe', methods=['POST'])
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

        # Prompt template
        prompt = f"Provide a clear and simple explanation for:\n{user_input}"

        logging.info(f"Describe input: {user_input}")

        response = get_groq_response(prompt)

        return jsonify({
            "status": "success",
            "response": response,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------------
# GENERATE REPORT ENDPOINT
# -------------------------------
@app.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        user_input = data['text']

        if user_input.strip() == "":
            return jsonify({"error": "Text cannot be empty"}), 400

        logging.info(f"Report input: {user_input}")

        # Structured prompt
        prompt = f"""
        Based on the following input, generate a structured report in JSON format.

        Input: {user_input}

        Output JSON format:
        {{
          "title": "",
          "executive_summary": "",
          "overview": "",
          "top_items": [],
          "recommendations": []
        }}
        """

        response = get_groq_response(prompt)

        # Try parsing JSON
        try:
            report_json = json.loads(response)
        except:
            report_json = {"raw_output": response}

        return jsonify({
            "status": "success",
            "report": report_json,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)