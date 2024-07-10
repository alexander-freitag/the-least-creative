# Description: This script is used to handle the user queries and generate the output file with the results.
# It takes the user query, detects the language, translates it to English if needed, extracts keywords, ranks the articles based on the keywords, and saves the results to a JSON file.

import requests
import time
import argparse
import json

from translation import translate_german_to_english, translate_bulgarian_to_english, detect_language
from keyword_extractor import extract_keywords
from handle_articles import format_all_articles


def rank_articles(generated_queries):
    system_prompt = """
        Rank the following articles based on their relevance to the user query.
        Use only the articles that are most relevant to the user query.
        If there are a lot of relevant articles, you can use the 10 articles.
        Return only the IDs of the articles in descending order of relevance.
        Order the ids in a comma-separated list.
        Do not include any additional information."""

    article_string = format_all_articles()
    user_prompt = "User Query: " + ", ".join(generated_queries) + "\n\n" + "Articles: " + "\n".join(article_string)

    ranking_data = {
        "model": "llama3",
        "raw": False,
        "prompt": f"{user_prompt}",
        "system": f"{system_prompt}",
        "stream": False,
    }

    ranking_response = requests.post("http://localhost:11434/api/generate", json=ranking_data)
    ranking_response = ranking_response.json()
    ranking_response = ranking_response["response"]

    return ranking_response

def handle_user_query(query, query_id, output_path):    
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
    ranked = rank_articles(detected_keywords)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    result = {
        'id': query_id,
        'query': query,
        'timestamp': timestamp,
        'detected_keywords': detected_keywords,
        'detected_language': detected_language,
        'rank_articles': ranked
    }
 
    with open(output_path, "w", encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)

    return result

# This is a sample argparse-setup, you probably want to use in your project:
parser = argparse.ArgumentParser(description='Run the inference.')
parser.add_argument('--query', type=str, help='The user query.', required=True, action="append")
parser.add_argument('--query_id', type=str, help='The IDs for the queries, in the same order as the queries.', required=True, action="append")
parser.add_argument('--output', type=str, help='Path to the output directory.', required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    queries = args.query
    query_ids = args.query_id
    output = args.output
    
    assert len(queries) == len(query_ids), "The number of queries and query IDs must be the same."
    
    for query, query_id in zip(queries, query_ids):
        handle_user_query(query, query_id, output)