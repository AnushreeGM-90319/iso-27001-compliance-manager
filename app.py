from flask import Flask, request, jsonify, Response, stream_with_context
from datetime import datetime
from services.groq_client import get_groq_response
from services.embedding_model import embedding_model
from services.cache import redis_client

import json
import time

app = Flask(__name__)


# ---------------------------------------------------
# HOME ROUTE
# ---------------------------------------------------
@app.route('/')
def home():
    return jsonify({
        "message": "API is running!"
    })


# ---------------------------------------------------
# DESCRIBE ENDPOINT
# ---------------------------------------------------
@app.route('/describe', methods=['POST'])
def describe():
    try:
        data = request.get_json(silent=True)

        # validate JSON
        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # validate text field
        if 'text' not in data:
            return jsonify({
                "error": "Missing 'text' field"
            }), 400

        user_input = data['text']

        # validate empty text
        if user_input.strip() == "":
            return jsonify({
                "error": "Text cannot be empty"
            }), 400

        # Redis cache check
        cache_key = f"describe:{user_input}"

        if redis_client:
            cached_response = redis_client.get(cache_key)

            if cached_response:
                return jsonify({
                    "status": "success",
                    "response": cached_response,
                    "cached": True,
                    "generated_at": datetime.utcnow().isoformat()
                })

        # optimized shorter prompt
        prompt = f"""
        Explain briefly:
        {user_input}
        """

        response = get_groq_response(prompt)

        # save to Redis cache
        if redis_client:
            redis_client.set(cache_key, response, ex=3600)

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


# ---------------------------------------------------
# GENERATE REPORT ENDPOINT
# ---------------------------------------------------
@app.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json(silent=True)

        # validate JSON
        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # validate text field
        if 'text' not in data:
            return jsonify({
                "error": "Missing 'text' field"
            }), 400

        user_input = data['text']

        # validate empty text
        if user_input.strip() == "":
            return jsonify({
                "error": "Text cannot be empty"
            }), 400

        # optimized shorter prompt
        prompt = f"""
        Generate report for:
        {user_input}

        Return:
        title,
        summary,
        overview,
        recommendations
        """

        response = get_groq_response(prompt)

        try:
            report_data = json.loads(response)

        except Exception:
            report_data = {
                "title": "Generated Report",
                "executive_summary": response,
                "overview": response,
                "top_items": [],
                "recommendations": []
            }

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


# ---------------------------------------------------
# GENERATE REPORT STREAMING
# ---------------------------------------------------
@app.route('/generate-report-stream')
def generate_report_stream():

    user_input = request.args.get('text')

    if not user_input:
        return "Please provide text using ?text=your_input"

    def generate():
        try:

            prompt = f"""
            Generate report for:
            {user_input}
            """

            response = get_groq_response(prompt)

            for word in response.split():
                yield f"data: {word}\n\n"
                time.sleep(0.03)

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

    return Response(
        stream_with_context(generate()),
        content_type='text/event-stream'
    )


# ---------------------------------------------------
# ANALYSE DOCUMENT
# ---------------------------------------------------
@app.route('/analyse-document', methods=['POST'])
def analyse_document():
    try:
        data = request.get_json(silent=True)

        # validate JSON
        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # validate text field
        if 'text' not in data:
            return jsonify({
                "error": "Missing 'text' field"
            }), 400

        user_input = data['text']

        # validate empty text
        if user_input.strip() == "":
            return jsonify({
                "error": "Text cannot be empty"
            }), 400

        # optimized shorter prompt
        prompt = f"""
        Analyze document:
        {user_input}

        Return findings with:
        type,
        description,
        severity
        """

        response = get_groq_response(prompt)

        try:
            parsed = json.loads(response)
            findings = parsed.get("findings", [])

        except Exception:
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


# ---------------------------------------------------
# BATCH PROCESS
# ---------------------------------------------------
@app.route('/batch-process', methods=['POST'])
def batch_process():
    try:
        data = request.get_json(silent=True)

        # validate JSON
        if not data:
            return jsonify({
                "error": "Request body must be JSON"
            }), 400

        # validate items field
        if 'items' not in data:
            return jsonify({
                "error": "Missing 'items' field"
            }), 400

        items = data['items']

        # validate list
        if not isinstance(items, list):
            return jsonify({
                "error": "'items' must be a list"
            }), 400

        # limit items
        if len(items) > 20:
            return jsonify({
                "error": "Maximum 20 items allowed"
            }), 400

        results = []

        for item in items:

            # 100ms delay
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


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)