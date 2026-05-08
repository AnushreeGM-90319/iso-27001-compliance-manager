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
@app.route('/analyse-document', methods=['POST'])
def analyse_document():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # ✅ validation
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        user_input = data['text']

        if user_input.strip() == "":
            return jsonify({"error": "Text cannot be empty"}), 400

        # 🧠 Prompt for structured output
        prompt = f"""
        Analyze the following document and extract key insights and risks.

        Document:
        {user_input}

        Return output strictly in JSON format:
        {{
          "findings": [
            {{
              "type": "insight or risk",
              "description": "brief explanation",
              "severity": "low/medium/high"
            }}
          ]
        }}
        """

        response = get_groq_response(prompt)

        # 🔧 Try parsing JSON
        try:
            parsed = json.loads(response)
            findings = parsed.get("findings", [])
        except:
            findings = [{
                "type": "unknown",
                "description": response,
                "severity": "low"
            }]

        return jsonify({
            "status": "success",
            "findings": findings,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@app.route('/batch-process', methods=['POST'])
def batch_process():
    try:
        data = request.get_json(silent=True)

        # ✅ validate JSON
        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # ✅ validate items field
        if 'items' not in data:
            return jsonify({
                "error": "Missing 'items' field"
            }), 400

        items = data['items']

        # ✅ validate list
        if not isinstance(items, list):
            return jsonify({
                "error": "'items' must be a list"
            }), 400

        # ✅ limit max 20 items
        if len(items) > 20:
            return jsonify({
                "error": "Maximum 20 items allowed"
            }), 400

        results = []

        # ✅ process each item
        for item in items:

            # simulate processing delay
            time.sleep(0.1)

            results.append({
                "input": item,
                "processed_result": f"Processed: {item}"
            })

        return jsonify({
            "status": "success",
            "results": results,
            "total_processed": len(results)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
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
        # ✅ safely read JSON
        data = request.get_json(silent=True)

        # ✅ check if request body exists
        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # ✅ check text field
        if 'text' not in data:
            return jsonify({
                "error": "Missing 'text' field"
            }), 400

        user_input = data['text']

        # ✅ empty text validation
        if user_input.strip() == "":
            return jsonify({
                "error": "Text cannot be empty"
            }), 400

        # ✅ AI prompt
        prompt = f"""
        Generate a structured report for the following topic:

        {user_input}

        Return output in JSON format with:
        - title
        - executive_summary
        - overview
        - top_items
        - recommendations
        """

        # ✅ get AI response
        response = get_groq_response(prompt)

        # ✅ try converting AI response to JSON
        try:
            report_data = json.loads(response)

        except Exception:
            # fallback if AI gives plain text
            report_data = {
                "title": "Generated Report",
                "executive_summary": response,
                "overview": response,
                "top_items": [],
                "recommendations": []
            }

        # ✅ final response
        return jsonify({
            "status": "success",
            "report": report_data,
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