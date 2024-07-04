from langdetect import detect, DetectorFactory, LangDetectException

# Ensure consistent results
DetectorFactory.seed = 0


def detect_language(text):
    try:
        # Detect the language of the input text
        detected_lang = detect(text)
        lang_map = {
            'en': 'en',
            'de': 'de',
            'bg': 'bg'
        }
        # Returns "en", "de", "bg" or "unknown" for a language that could not be detected
        return lang_map.get(detected_lang, 'Unknown')
    except LangDetectException:
        return 'Unknown'