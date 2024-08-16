import sounddevice as sd
import wavio
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import langdetect

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

# Function to record audio
def record_audio(filename, duration=5, fs=44100):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Recording complete.")

# Function to recognize speech and detect language
def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            lang = langdetect.detect(text)
            return text, lang
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None, None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return None, None

# Function to translate text
def translate_text(text, src_lang, dest_lang):
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

# Function to convert text to speech and play it
def text_to_speech(text, lang):
    tts = gTTS(text, lang=lang)
    tts.save("./test_recording/output.mp3")
    audio = AudioSegment.from_mp3("./test_recording/output.mp3")
    play(audio)
    os.remove("./test_recording/output.mp3")

# Main function to handle the conversation
def two_way_translation():
    user1_lang = None
    user2_lang = None

    while True:
        # User 1's turn
        print("User 1, please speak:")
        record_audio("./test_recording/user1_input.wav")
        user1_text, detected_lang1 = recognize_speech("./test_recording/user1_input.wav")
        
        if user1_text:
            if not user1_lang:
                user1_lang = detected_lang1
                print(f"User 1's language detected as: {languages.get(user1_lang, user1_lang)}")
            
            print(f"User 1 said: {user1_text}")
            
            if user2_lang:
                translated_text = translate_text(user1_text, user1_lang, user2_lang)
                print(f"Translated for User 2: {translated_text}")
                text_to_speech(translated_text, user2_lang)
        
        # User 2's turn
        print("User 2, please speak:")
        record_audio("./test_recording/user2_input.wav")
        user2_text, detected_lang2 = recognize_speech("./test_recording/user2_input.wav")
        
        if user2_text:
            if not user2_lang:
                user2_lang = detected_lang2
                print(f"User 2's language detected as: {languages.get(user2_lang, user2_lang)}")
            
            print(f"User 2 said: {user2_text}")
            
            if user1_lang:
                translated_text = translate_text(user2_text, user2_lang, user1_lang)
                print(f"Translated for User 1: {translated_text}")
                text_to_speech(translated_text, user1_lang)

        # Ask if users want to continue
        continue_conversation = input("Do you want to continue the conversation? (yes/no): ").lower()
        if continue_conversation != 'yes':
            break

# Run the function
two_way_translation()   