# implementing for voice basis working for one user.

import sounddevice as sd
import wavio
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# Initialize the translator
translator = Translator()

# Supported languages dictionary
languages = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-cn': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'ja': 'Japanese'
}

# Default source language (user's spoken language)
default_src_lang = 'hi'  # Adapt this based on the user's language preference
default_dest_lang = 'en'  # Default translation target language is English

# Function to record audio
def record_audio(filename, duration=3, fs=8000):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until the recording is finished
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Recording complete.")

# Function to recognize speech and translate
def recognize_and_translate():
    audio_filename = "./test_recording/input.wav"
    
    # Record audio from the microphone
    record_audio(audio_filename)
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_filename) as source:
        audio = recognizer.record(source)
        
        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio, language=default_src_lang)
            print(f"Recognized text: {text}")
            
            # Translate the recognized text
            translated_text = translator.translate(text, src=default_src_lang, dest=default_dest_lang).text
            print(f"Translation to {languages[default_dest_lang]}: {translated_text}")
            
            # Convert translated text to speech
            tts = gTTS(translated_text, lang=default_dest_lang)
            tts.save("./test_recording/translated.mp3")
            
            # Play the translated speech
            translated_audio = AudioSegment.from_mp3("./test_recording/translated.mp3")
            play(translated_audio)
            os.remove("./test_recording/translated.mp3")
            
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")

# Run the function
recognize_and_translate()
