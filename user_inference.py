import requests as r
import time

from os.path import join
from language_detection import detect_language
from translation import translate_german_to_english, translate_bulgarian_to_english
from keyword_extractor import extract_keywords
from handle_queries import save_query
from handle_articles import format_all_articles


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
    detected_keywords = extract_keywords(translated_query)
    
    # Ranking the articles based on the keywords
    rank_articles = rank_articles(detected_keywords)
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


def rank_articles(generated_queries):
    system_prompt = """
        Rank the following articles based on their relevance to the user query.
        Use only the articles that are most relevant to the user query.
        If there are a lot of relevant articles, you can use the 10 articles.
        Return only the IDs of the articles in descending order of relevance.
        Order the ids in a comma-separated list.
        Do not include any additional information."""

    article_string = format_all_articles()
    user_prompt = "User Query: " + generated_queries + "\n\n" + "Articles: " + "\n".join(article_string)

    ranking_data = {
        "model": "llama3",
        "raw": False,
        "prompt": f"{user_prompt}",
        "system": f"{system_prompt}",
        "stream": False,
    }

    ranking_response = r.post("http://localhost:11434/api/generate", json=ranking_data)
    ranking_response = ranking_response.json()
    ranking_response = ranking_response["response"]

    return ranking_response