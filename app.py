from flask import Flask, request, jsonify, send_file, send_from_directory, make_response
from flask_cors import CORS, cross_origin
#from gtts import gTTS
#from TTS.api import TTS
import uuid
import os
from utils.qa import qa_with_fallback
from utils.tts import call_tts
import edge_tts
import asyncio
import tempfile
import time

app = Flask(__name__, static_folder="audio", static_url_path="/audio")
TTS_SERVICE_URL = "http://tts-service:6000/speak"

# ✅ CORS bien configuré — autorise localhost:8000
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}}, supports_credentials=True)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

FILE_NAME = "audio.wav"  # nom fixe
FILE_PATH = os.path.join(AUDIO_DIR, FILE_NAME)


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
    
    
    asyncio.run(synthesize(llm_response, FILE_PATH))        
    # filename = f"{uuid.uuid4()}.mp3"
    # filepath = os.path.join(AUDIO_DIR, filename)
    # os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    #call_tts(llm_response) 
    audio_url = f"/audio/{FILE_NAME}?t={int(time.time())}"  
    return jsonify({
        "response": llm_response,
        "audio_path": audio_url
    })

async def synthesize(text, file_path):
    communicate = edge_tts.Communicate(text, voice="fr-FR-DeniseNeural")
    await communicate.save(file_path)

@app.route("/audio/<filename>")
@cross_origin()  # ← ajoute les bons en-têtes CORS
def serve_audio(filename):
    path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="audio/mpeg", conditional=True)
    return "Not found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
