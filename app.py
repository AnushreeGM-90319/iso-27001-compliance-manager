from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes.describe import describe_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(describe_bp)

# Health check
@app.route("/health")
def health():
    return {"status": "ok"}

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)