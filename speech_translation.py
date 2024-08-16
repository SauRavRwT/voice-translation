import sounddevice as sd
import wavio
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from langdetect import detect
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# Initialize the translator
translator = Translator()

# Function to record audio
def record_audio(filename, duration=5, fs=16000):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until the recording is finished
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Recording complete.")

# Function to detect the language of text using langdetect
def detect_language(text):
    try:
        detected_lang = detect(text)
        detected_language_name = LANGUAGES.get(detected_lang, 'Unknown')
        print(f"Detected language: {detected_language_name}")
        return detected_lang
    except:
        print("Language detection failed.")
        return None

# Function to recognize speech and translate based on detected language
def recognize_and_translate(user_label, target_lang):
    audio_filename = f"./test_recording/input_{user_label}.wav"
    
    # Record audio from the microphone
    record_audio(audio_filename)
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_filename) as source:
        audio = recognizer.record(source)
        
        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            print(f"{user_label} said: {text}")
            
            # Detect the language of the recognized text
            src_lang = detect_language(text)
            if src_lang is None:
                print(f"{user_label}: Could not detect language. Skipping translation.")
                return None, None
            
            # Translate the recognized text to the target language
            translated_text = translator.translate(text, src=src_lang, dest=target_lang).text
            print(f"Translation to {LANGUAGES.get(target_lang, 'Unknown')}: {translated_text}")
            
            # Convert translated text to speech
            tts = gTTS(translated_text, lang=target_lang)
            translated_audio_file = f"./test_recording/translated_{user_label}.mp3"
            tts.save(translated_audio_file)
            
            # Play the translated speech
            translated_audio = AudioSegment.from_mp3(translated_audio_file)
            play(translated_audio)
            os.remove(translated_audio_file)
            
            return src_lang, target_lang
        
        except sr.UnknownValueError:
            print(f"{user_label}: Could not understand the audio.")
        except sr.RequestError as e:
            print(f"{user_label}: Error with the speech recognition service; {e}")
        
        return None, None

# Function to manage conversation between two users
def conversation():
    # Placeholder for the detected languages of both users
    user_1_lang = None
    user_2_lang = None
    
    while True:
        print("\nListening to User 1...")
        if user_2_lang:
            # Translate User 1's input to User 2's language
            user_1_lang, _ = recognize_and_translate("User 1", user_2_lang)
        else:
            # Identify and store User 1's language in the first round
            user_1_lang, _ = recognize_and_translate("User 1", "en")  # Default to English if no language is detected

        print("\nListening to User 2...")
        if user_1_lang:
            # Translate User 2's input to User 1's language
            user_2_lang, _ = recognize_and_translate("User 2", user_1_lang)
        else:
            # Identify and store User 2's language in the first round
            user_2_lang, _ = recognize_and_translate("User 2", "en")  # Default to English if no language is detected
        
        # Option to continue or end the conversation
        cont = input("\nDo you want to continue the conversation? (yes/no): ").strip().lower()
        if cont != 'yes':
            break

# Run the conversation
conversation()
