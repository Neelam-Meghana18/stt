import speech_recognition as sr
from pydub import AudioSegment

# Convert mp3 to wav if needed (Google SpeechRecognition works best with wav)
audio = AudioSegment.from_file("test.mp3")
audio.export("input.wav", format="wav")

# Initialize recognizer
r = sr.Recognizer()

# Load the audio file
with sr.AudioFile("input.wav") as source:
    print("Listening...")
    audio_data = r.record(source)
    
    # Recognize (convert from speech to text)
    try:
        text = r.recognize_google(audio_data)
        print("Transcribed Text:")
        print(text)
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
