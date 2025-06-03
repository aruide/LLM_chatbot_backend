#from edgetts import Communicate
from flask import Flask, request, jsonify, send_file, send_from_directory, make_response

def call_tts(message):
    url = "http://localhost:6000/speak"
    payload = {"text": message}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        with open("audio/audio.wav", "wb") as f:
            f.write(response.content)            
