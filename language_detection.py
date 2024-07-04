from langdetect import detect, DetectorFactory, LangDetectException

# Ensure consistent results
DetectorFactory.seed = 0


def detect_language(text):
    try:
        # Detect the language of the input text
        detected_lang = detect(text)
        lang_map = {
            'de': 'de',
            'en': 'en',
            'bg': 'bg'
        }
        # Return either "Bulgarian", "German", "English" or "Unknown" if it isn't one of the three languages.
        return lang_map.get(detected_lang, 'Unknown')
    except LangDetectException:
        return 'Unknown'