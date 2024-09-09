from flask import Flask, request, jsonify, send_file
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import pygame

app = Flask(__name__)

def translate_text(text, source_lang, target_lang):
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def get_voice_input(language):
    recognizer = sr.Recognizer()
    lang_code = f"{language.lower()}"

    with sr.Microphone() as source:
        print(f"Listening for voice input in {language}...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language=lang_code)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return None

def speak_text(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with BytesIO() as audio_file:
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            return audio_file
    except Exception as e:
        print(f"Error with TTS conversion: {e}")
        return None

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    
    if text and source_lang and target_lang:
        translated_text = translate_text(text, source_lang, target_lang)
        return jsonify({"translated_text": translated_text})
    return jsonify({"error": "Invalid input"}), 400

@app.route('/voice-input', methods=['POST'])
def voice_input():
    data = request.json
    language = data.get('language')
    
    if language:
        text = get_voice_input(language)
        return jsonify({"text": text})
    return jsonify({"error": "Invalid input"}), 400

@app.route('/speak-text', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text')
    lang = data.get('lang', 'en')
    
    if text:
        audio_file = speak_text(text, lang)
        if audio_file:
            return send_file(audio_file, mimetype='audio/mpeg')
    return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True)
