# Description: This file contains the code to extract keywords from a given text using the Ollama API with the Llama3 model.

import requests

# Extracting keywords using Ollama with the Llama3 model
def extract_keywords_ollama(text):
    
    # Sending a request to the Ollama API to extract keywords
    keywords_data = {
        "model": "llama3",
        "prompt": "User Query: " + text,
        "system": """
            You will receive a user query in English.
            Enhance the search query to ensure it is clear, context-rich, and unbiased.
            Additionally, identify and extract the most relevant tags related to the query.
            Return only the generated tags on the first line and on one line, separated by commas.
            Do not include any additional information.
            Do not add any punctuation at the end of the line.
            Do not add titles or headers.
            Do not show the user query or the enhanced user query.""",
        "stream": False
    }
    keywords_response = requests.post("http://localhost:11434/api/generate", json=keywords_data)
    keywords_response = keywords_response.json()
    keywords_response = keywords_response["response"]

    # Extracting keywords from the response
    keywords = [keyword.strip() for keyword in keywords_response.split(",")]

    return keywords


def extract_keywords(text):
    return extract_keywords_ollama(text)
