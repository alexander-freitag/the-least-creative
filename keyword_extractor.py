import requests as r

# Extracting keywords using Ollama with the Llama3 model
def extract_keywords_ollama(text):
    
    # Sending a request to the Ollama API to extract keywords
    keywords_data = {
        "model": "llama3",
        "prompt": "User Query: " + text,
        "system": """
            You will reacieve a user query in English.
            Enhance the search query to ensure it is clear, context-rich, and unbiased.
            Additionally, identify and extract the most relevant tags related to the query.
            Return only the generated tags on the first line and on one line, separated by commas.
            Do not include any additional information.
            Do not add any punctuation at the end of the line.
            Do not add titles or headers.
            Do not show the user query or the enhanced user query.""",
        "stream": False
    }
    keywords_response = r.post("http://localhost:11434/api/generate", json=keywords_data)
    keywords_response = keywords_response.json()
    keywords_response = keywords_response["response"]

    # Extracting keywords from the response
    keywords = keywords_response.split(", ")

    return keywords


# import torch
# from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

# # Load the fine-tuned model
# model_path = 'training/results'
# model = AutoModelForTokenClassification.from_pretrained(model_path)
# tokenizer = AutoTokenizer.from_pretrained(model_path)

# # Create a pipeline for token classification
# keyword_extractor = pipeline(
#     task="token-classification",
#     model=model,
#     tokenizer=tokenizer,
#     device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
# )

# def extract_keywords_trained(text):
#     # Extract keywords from the text
#     keywords = keyword_extractor(text)
#     return [keyword['word'] for keyword in keywords]

