from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.qa import qa_with_fallback

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = qa_with_fallback(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(port=5000)