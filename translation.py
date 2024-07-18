# Description: This file contains the functions to translate German and Bulgarian text to English using the Helsinki-NLP models.
# It also includes a function to detect the language of the input text.

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langdetect import DetectorFactory, LangDetectException, detect

from user_config import BG_MODEL_PATH, DE_MODEL_PATH

# Load the fine-tuned model and tokenizer

# Load the fine-tuned model and tokenizer
model_de = AutoModelForSeq2SeqLM.from_pretrained(DE_MODEL_PATH)
tokenizer_de = AutoTokenizer.from_pretrained(DE_MODEL_PATH)
model_bg = AutoModelForSeq2SeqLM.from_pretrained(BG_MODEL_PATH)
tokenizer_bg = AutoTokenizer.from_pretrained(BG_MODEL_PATH)
device = 0 if torch.cuda.is_available() else -1
# Create a translation pipeline
translation_pipeline_de_en = pipeline("translation_de_to_en", model=model_de, tokenizer=tokenizer_de, device=device)
translation_pipeline_bg_en = pipeline("translation_bg_to_en", model=model_bg, tokenizer=tokenizer_bg, device=device)


def split_text_by_periods(text, num_periods=5):
    # Split the text into chunks based on the number of periods
    sentences = text.split('. ')
    chunks = []

    for i in range(0, len(sentences), num_periods):
        chunk = '. '.join(sentences[i:i + num_periods])
        if chunk[-1] != '.':
            chunk += '.'
        chunks.append(chunk)

    return chunks


# Function to translate German text to English
def translate_german_to_english(german_text):
    translated_text = []
    for sentence in split_text_by_periods(german_text):
        translated_text.append(translation_pipeline_de_en(sentence))
    return "".join(e[0]['translation_text'] for e in translated_text)


# Function to translate Bulgarian text to English
def translate_bulgarian_to_english(bulgarian_text):
    translated_text = []
    for sentence in split_text_by_periods(bulgarian_text):
        translated_text.append(translation_pipeline_bg_en(sentence))
    return "".join(e[0]['translation_text'] for e in translated_text)


# Ensure consistent results for language detection
DetectorFactory.seed = 0

def detect_language(text):
    # text = split_text_by_periods(text)[0]

    try:
        # Detect the language of the input text
        detected_lang = detect(text)
        lang_map = {
            'de': 'de',
            'bg': 'bg'
        }
        # Return either "bg", "de", "en" or "unknown" if it isn't one of the three languages.
        return lang_map.get(detected_lang, 'en')
    except LangDetectException:
        return 'en'
