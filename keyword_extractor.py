import torch
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

# Load the fine-tuned model
model_path = 'training/results'
model = AutoModelForTokenClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Create a pipeline for token classification
keyword_extractor = pipeline(
    task="token-classification",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
)

def extract_keywords(text):
    # Extract keywords from the text
    keywords = keyword_extractor(text)
    return [keyword['word'] for keyword in keywords]
