from googletrans import Translator

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

# Function to translate text
def translate_text():
    # Ask user for input text
    text = input(f"Enter the text you want to translate from {languages[default_src_lang]}: ")

    # Display the supported languages
    print("Supported languages:")
    for code, lang in languages.items():
        print(f"{code}: {lang}")

    # Ask user for target language, default to English
    dest_lang = input("Enter the target language code (default is 'en' for English): ").strip().lower() or 'en'

    if dest_lang not in languages:
        print("Invalid target language code.")
        return

    # Perform translation
    translated = translator.translate(text, src=default_src_lang, dest=dest_lang).text
    print(f"Translation from {languages[default_src_lang]} to {languages[dest_lang]}: {translated}")

# Run the function
translate_text()
