from flask import Flask, request, jsonify, send_file, send_from_directory, make_response
from flask_cors import CORS, cross_origin
#from gtts import gTTS
#from TTS.api import TTS
import uuid
import os
from utils.qa import qa_with_fallback
#from utils.tts import texte_to_speech

app = Flask(__name__, static_folder="audio", static_url_path="/audio")

# ✅ CORS bien configuré — autorise localhost:8000
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}}, supports_credentials=True)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Charger une instance TTS une fois au lancement
# Ici un modèle français basique, tu peux changer par le modèle que tu veux
#tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=False, gpu=False)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    print(f"[User]: {user_input}")

    llm_response = qa_with_fallback(user_input)
    print(f"[LLM]: {llm_response}")

    # filename = f"{uuid.uuid4()}.mp3"
    # filepath = os.path.join(AUDIO_DIR, filename)
    # os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    #filename = texte_to_speech(llm_response)   
    filename = "rien"
    return jsonify({
        "response": llm_response,
        "audio_path": f"/audio/{filename}"
    })

# @app.route("/api/tts", methods=["POST"])
# def tts():
#     text = request.json.get("text", "")
#     audio_id = str(uuid.uuid4())
#     audio_path = os.path.join(AUDIO_DIR, f"{audio_id}.mp3")

#     #generate_gtts(text, audio_path)
#     return jsonify({"audio_url": f"/api/audio/{audio_id}.mp3"})

@app.route("/audio/<filename>")
@cross_origin()  # ← ajoute les bons en-têtes CORS
def serve_audio(filename):
    path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="audio/mpeg", conditional=True)
    return "Not found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
