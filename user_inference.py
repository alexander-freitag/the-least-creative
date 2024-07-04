from os.path import join
from translation import translate_german_to_english, translate_bulgarian_to_english
from keyword_extractor import extract_keywords_ollama
from scripts.handle_articles import format_all_articles
from scripts.handle_queries import save_query
from language_detection import detect_language

import argparse
import requests as r
import time


def handle_user_query(query):    
    # Detecting the language of the query
    detected_language = detect_language(query)

    # Translating the query to English if needed
    if detected_language == "de":
        translated_query = translate_german_to_english(query)
    elif detected_language == "bg":
        translated_query = translate_bulgarian_to_english(query)
    elif detected_language == "en":
        translated_query = query
    else:
        raise ValueError("Language not supported or recognized")

    # Extracting keywords from the translated query
    detected_keywords = extract_keywords_ollama(translated_query)
    
    # Ranking the articles based on the keywords
    # TODO rank_articles = rank_articles(detected_keywords)
    rank_articles = []

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Save the JSON data to the file
    id = save_query(query, timestamp, detected_keywords, detected_language, rank_articles)
    
    result = {
        'id': id,
        'query': query,
        'timestamp': timestamp,
        'detected_keywords': detected_keywords,
        'detected_language': detected_language,
        'rank_articles': rank_articles
    }
 
    return result

# test_query = """
# What are the benefits of LLMs in programming?
# """
# handle_user_query(test_query)

