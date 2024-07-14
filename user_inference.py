# Description: This script is used to handle the user queries and generate the output file with the results.
# It takes the user query, detects the language, translates it to English if needed, extracts keywords, ranks the articles based on the keywords, and saves the results to a JSON file.
# The output file contains the query, detected language, translated query, generated query, and suggested articles.
# The output file is saved in the output directory with the query ID as the filename.

import math
import os
import time
import argparse
import json

from collections import defaultdict, Counter
from dataset import load_dataset
from translation import translate_german_to_english, translate_bulgarian_to_english, detect_language
from keyword_extractor import extract_keywords
from user_config import QUERIES_PATH

# Function to rank articles based on the generated queries
# It takes the generated queries and the articles as input
# The "articles" parameter should be a list of dictionaries with 'id', 'title', 'content', and 'transformed_representation' keys
# It returns the top N ranked articles based on the TF-IDF scores
def rank_articles(generated_queries, articles, top=10):
    # Step 1: Inverted Index Creation
    inverted_index = defaultdict(set)
    for article in articles:
        for keyword in article['transformed_representation']:
            inverted_index[keyword.lower()].add(article['id'])

    # Step 2: Retrieve Matching Articles
    def retrieve_articles(query_keywords):
        matching_articles = set()
        for keyword in query_keywords:
            if keyword in inverted_index:
                matching_articles.update(inverted_index[keyword])
        return matching_articles

    # Replace with actual query keywords extraction
    matching_article_ids = retrieve_articles(generated_queries)
    matching_articles = [article for article in articles if article['id'] in matching_article_ids]

    # Step 3: TF-IDF Calculation
    def compute_tf(article):
        tf = Counter(article['transformed_representation'])
        total_terms = len(article['transformed_representation'])
        return {term: freq / total_terms for term, freq in tf.items()}

    def compute_idf(articles):
        num_articles = len(articles)
        idf = defaultdict(lambda: 0)
        for article in articles:
            unique_terms = set(article['transformed_representation'])
            for term in unique_terms:
                idf[term] += 1
        return {term: math.log(num_articles / (freq + 1)) for term, freq in idf.items()}

    def compute_tf_idf(articles):
        idf = compute_idf(articles)
        tf_idf = {}
        for article in articles:
            tf = compute_tf(article)
            tf_idf[article['id']] = {term: tf_val * idf[term] for term, tf_val in tf.items()}
        return tf_idf

    tf_idf_scores = compute_tf_idf(articles)

    # Step 4: Rank Articles
    def rank_articles(query_keywords, tf_idf_scores):
        article_scores = defaultdict(lambda: 0)
        for article_id, scores in tf_idf_scores.items():
            for keyword in query_keywords:
                if keyword in scores:
                    article_scores[article_id] += scores[keyword]
        ranked_articles = sorted(article_scores.items(), key=lambda item: item[1], reverse=True)
        return ranked_articles

    ranked_article_ids = rank_articles(generated_queries, tf_idf_scores)
    ranked_articles = [article for article_id, score in ranked_article_ids for article in articles if
                       article['id'] == article_id]

    # Step 5: Return Top N Articles
    if len(ranked_articles) < top:
        return ranked_articles
    else:
        top_articles = ranked_articles[:top]
        return top_articles


# Function to print the results of the user query
def print_results(query_id, query, detected_language, translated_query, generated_query, suggested_queries):
    print(f"Query ID: {query_id}")
    print(f"Query: {query}")
    print(f"Detected Language: {detected_language}")
    print(f"Translated Query: {translated_query}")
    print(f"Generated Query: {generated_query}")
    print("\nSuggested Articles:")
    for i, article in enumerate(suggested_queries, 1):
        print(f"{i}. Title: {article['title']}")
        print(f"   Content: {article['content']}")
        print(f"   Keywords: {article['transformed_representation']}")
        print("")
    print("")


# Function to handle the user query
# It takes the user query, query ID, and the output path as input
# Is saves the processed results to a JSON file in the output directory
def handle_user_query(query, query_id, output_path):
    # Detecting the language of the query
    detected_language = detect_language(query)

    if detected_language == "unknown":
        raise ValueError("Language not supported or recognized. Please provide a query in English, German, or Bulgarian.")

    # Translating the query to English if needed
    # Extracting keywords from the query or from the translation if one was performed
    if detected_language == "de":
        translated_query = translate_german_to_english(query)
        detected_keywords = extract_keywords(translated_query)
    elif detected_language == "bg":
        translated_query = translate_bulgarian_to_english(query)
        detected_keywords = extract_keywords(translated_query)
    elif detected_language == "en":
        translated_query = ""
        detected_keywords = extract_keywords(query)
    else:
        raise ValueError("Language not supported or recognized")

    # Loading the dataset
    articles = load_dataset()

    # Ranking the articles based on the keywords
    suggested_queries = rank_articles(detected_keywords, articles, top=10)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    result = {
        'id': query_id,
        'timestamp': timestamp,
        'query': query,
        'detected_language': detected_language,
        'translated_query': translated_query,
        'generated_query': detected_keywords,
        'suggested_queries': suggested_queries
    } 
 
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(output_path, f"{query_id}.json")
    with open(output_file, "w", encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)

    print(f"Results saved to: {output_file}")
    print_results(query_id, query, detected_language, translated_query, detected_keywords, suggested_queries)

    return result

# This is a sample argparse-setup, you probably want to use in your project:
parser = argparse.ArgumentParser(description='Run the inference.')
parser.add_argument('--query', type=str, help='The user query.', required=True, action="append")
parser.add_argument('--query_id', type=str, help='The IDs for the queries, in the same order as the queries.', required=True, action="append")
parser.add_argument('--output', type=str, help='Path to the output directory.', default=QUERIES_PATH)

if __name__ == "__main__":
    args = parser.parse_args()
    queries = args.query
    query_ids = args.query_id
    output = args.output
    
    assert len(queries) == len(query_ids), "The number of queries and query IDs must be the same."
    
    for query, query_id in zip(queries, query_ids):
        if output is None:
            output = QUERIES_PATH
        handle_user_query(query, query_id, output)