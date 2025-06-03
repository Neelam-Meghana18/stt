from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import speech_recognition as sr
from langdetect import detect
from pydub import AudioSegment
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

# Set FFmpeg path
os.environ["PATH"] += os.pathsep + r"C:\Users\Neelam Meghana\ffmpeg\ffmpeg-7.1.1-essentials_build\bin"

# Set OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Save and convert uploaded file
        audio = request.files['audio_data']
        audio.save("input.webm")
        sound = AudioSegment.from_file("input.webm")
        sound.export("input.wav", format="wav")

        # Recognize speech
        r = sr.Recognizer()
        with sr.AudioFile("input.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            lang = detect(text)

        # Get LLM response from OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct",  # or another free model
            "messages": [
                {"role": "user", "content": text}
            ]
        }
        res = requests.post(OPENROUTER_API_URL, json=data, headers=headers)
        reply = res.json()['choices'][0]['message']['content'].strip()

        # Convert reply to speec
        tts = gTTS(text=reply, lang='en-au', slow=False)
        tts.save("static/output.mp3")

        return jsonify({'transcript': text, 'response': reply, 'language': lang})
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
