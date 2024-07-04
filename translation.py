import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Load the fine-tuned model and tokenizer
model_de = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")
tokenizer_de = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")
model_bg = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-bg-en")
tokenizer_bg = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-bg-en")

device = 0 if torch.cuda.is_available() else -1
# Create a translation pipeline
translation_pipeline_de_en = pipeline("translation_de_to_en", model=model_de, tokenizer=tokenizer_de, device=device)
translation_pipeline_bg_en = pipeline("translation_bg_to_en", model=model_bg, tokenizer=tokenizer_bg, device=device)


def split_text_by_periods(text, num_periods=5):
    # Sätze anhand von Punkt aufteilen
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
        translated_text.append(translation_pipeline_de_en(sentence))
    return "".join(e[0]['translation_text'] for e in translated_text)
