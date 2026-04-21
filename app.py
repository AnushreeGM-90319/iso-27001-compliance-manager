from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Service Running"

@app.route('/health')
def health():
    return {"status": "OK"}

if __name__ == "__main__":
    app.run(port=5000, debug=True)