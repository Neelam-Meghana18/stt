from gtts import gTTS

# Text you want to convert to speech
text = "Hello Meghana! This is a free Text to Speech example using gTTS."

# Create gTTS object
tts = gTTS(text=text, lang='en')

# Save audio to a file
tts.save("output.mp3")

print("Audio file saved as output.mp3")
