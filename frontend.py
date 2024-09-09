import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
from gtts import gTTS
from io import BytesIO
import pygame


# Function to translate text using Google Translator
def translate_text(text, source_lang, target_lang):
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


# Function to get voice input using SpeechRecognition
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


# Function to speak text using pyttsx3 or gTTS
def speak_text(text, lang='en'):
    if lang == 'en':
        # Use pyttsx3 for English
        engine = pyttsx3.init()
        engine.setProperty('voice', engine.getProperty('voices')[0].id)  # English
        engine.say(text)
        engine.runAndWait()
    else:
        # Use gTTS for other languages
        try:
            tts = gTTS(text=text, lang=lang)
            with BytesIO() as audio_file:
                tts.write_to_fp(audio_file)
                audio_file.seek(0)
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error with TTS conversion: {e}")


# Function for Text Translation GUI
def text_translation_gui():
    def translate_text_gui():
        source_lang = source_lang_combo.get()
        target_lang = target_lang_combo.get()
        text = text_entry.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Input Error", "Please enter some text to translate.")
            return

        try:
            translated_text = translate_text(text, source_lang, target_lang)
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, translated_text)
            result_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Translation Error", f"Error: {str(e)}")

    def speak_result():
        text = result_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "No text available to speak.")
        else:
            speak_text(text, lang=target_lang_combo.get())

    text_window = tk.Toplevel(root)
    text_window.title("Text Translation")

    # Language selection
    source_lang_label = tk.Label(text_window, text="Source Language:")
    source_lang_label.pack(pady=5)
    source_lang_combo = ttk.Combobox(text_window, values=list(target_lang_codes.keys()))
    source_lang_combo.pack(pady=5)

    target_lang_label = tk.Label(text_window, text="Target Language:")
    target_lang_label.pack(pady=5)
    target_lang_combo = ttk.Combobox(text_window, values=list(target_lang_codes.keys()))
    target_lang_combo.pack(pady=5)

    # Text input
    text_label = tk.Label(text_window, text="Enter text to translate:")
    text_label.pack(pady=5)
    text_entry = tk.Text(text_window, height=5, width=50)
    text_entry.pack(pady=5)

    # Translate button
    translate_button = tk.Button(text_window, text="Translate", command=translate_text_gui)
    translate_button.pack(pady=5)

    # Result display
    result_label = tk.Label(text_window, text="Translated text:")
    result_label.pack(pady=5)
    result_text = tk.Text(text_window, height=5, width=50, state=tk.DISABLED)
    result_text.pack(pady=5)

    # Speak button
    speak_button = tk.Button(text_window, text="Speak Translation", command=speak_result)
    speak_button.pack(pady=5)


# Function for Voice Translation GUI
def voice_translation_gui():
    def start_voice_translation():
        source_lang = source_lang_combo.get()
        target_lang = target_lang_combo.get()

        try:
            text = get_voice_input(source_lang)
            if text:
                translated_text = translate_text(text, source_lang, target_lang)
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, translated_text)
                result_text.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "No voice input detected.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during voice recognition: {str(e)}")

    def speak_result():
        text = result_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "No text available to speak.")
        else:
            speak_text(text, lang=target_lang_combo.get())

    voice_window = tk.Toplevel(root)
    voice_window.title("Voice Translation")

    # Language selection
    source_lang_label = tk.Label(voice_window, text="Source Language:")
    source_lang_label.pack(pady=5)
    source_lang_combo = ttk.Combobox(voice_window, values=list(target_lang_codes.keys()))
    source_lang_combo.pack(pady=5)

    target_lang_label = tk.Label(voice_window, text="Target Language:")
    target_lang_label.pack(pady=5)
    target_lang_combo = ttk.Combobox(voice_window, values=list(target_lang_codes.keys()))
    target_lang_combo.pack(pady=5)

    # Voice input button
    voice_button = tk.Button(voice_window, text="Start Voice Translation", command=start_voice_translation)
    voice_button.pack(pady=10)

    # Result display
    result_label = tk.Label(voice_window, text="Translated text:")
    result_label.pack(pady=5)
    result_text = tk.Text(voice_window, height=5, width=50, state=tk.DISABLED)
    result_text.pack(pady=5)

    # Speak button
    speak_button = tk.Button(voice_window, text="Speak Translation", command=speak_result)
    speak_button.pack(pady=5)


# Main function to choose between Text or Voice Translation
def main_gui():
    def open_translation_gui():
        choice = translation_choice.get()
        if choice == "text":
            text_translation_gui()
        elif choice == "voice":
            voice_translation_gui()

    global root
    root = tk.Tk()
    root.title("Translation Selector")

    translation_choice_label = tk.Label(root, text="Choose Translation Mode:")
    translation_choice_label.pack(pady=10)

    translation_choice = tk.StringVar(value="text")
    text_radio = tk.Radiobutton(root, text="Text Translation", variable=translation_choice, value="text")
    text_radio.pack(pady=5)
    voice_radio = tk.Radiobutton(root, text="Voice Translation", variable=translation_choice, value="voice")
    voice_radio.pack(pady=5)

    open_button = tk.Button(root, text="Open Translation", command=open_translation_gui)
    open_button.pack(pady=20)

    root.mainloop()


# Language codes dictionary
target_lang_codes = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese (Portugal, Brazil)": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}

# Run the main GUI
main_gui()
