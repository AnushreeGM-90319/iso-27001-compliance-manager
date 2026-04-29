from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from services.groq_client import get_groq_response
from datetime import datetime
import json
import logging
import time

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

@app.route('/generate-report-stream')
def generate_report_stream():
    user_input = request.args.get('text')

    if not user_input:
        return "Please provide text using ?text=your_input"

    def generate():
        try:
            prompt = f"""
            Generate a structured report for:
            {user_input}
            """

            full_response = get_groq_response(prompt)

            # Stream word-by-word (token simulation)
            for word in full_response.split():
                yield f"data: {word}\n\n"
                time.sleep(0.03)

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream"
    )
# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)