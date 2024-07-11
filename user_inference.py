# Description: This script is used to handle the user queries and generate the output file with the results.
# It takes the user query, detects the language, translates it to English if needed, extracts keywords, ranks the articles based on the keywords, and saves the results to a JSON file.

import math
from collections import defaultdict, Counter
import time
import argparse
import json

from handle_articles import get_all_articles
from translation import translate_german_to_english, translate_bulgarian_to_english, detect_language
from keyword_extractor import extract_keywords

def rank_articles(generated_queries):
    articles = get_all_articles()

    # Step 1: Inverted Index Creation
    inverted_index = defaultdict(set)
    for article in articles:
        for keyword in article['keywords']:
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
        tf = Counter(article['keywords'])
        total_terms = len(article['keywords'])
        return {term: freq / total_terms for term, freq in tf.items()}

    def compute_idf(articles):
        num_articles = len(articles)
        idf = defaultdict(lambda: 0)
        for article in articles:
            unique_terms = set(article['keywords'])
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

    # Step 5: Display Top-N Articles
    top_n = 10  # Number of top articles to display
    top_articles = ranked_articles[:top_n]
    ranking_response = ""
    for article in top_articles:
        ranking_response += f"1.\tTitle: {article['title']}\n\tContent: {article['content'][:200]}...\nKeywords: {article['keywords']}"
        print(f"Title: {article['title']}")
        print(f"Content: {article['content'][:200]}...")
        print(f"Keywords: {article['keywords']}...")  # Display first 200 characters of the content
        print("\n")

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