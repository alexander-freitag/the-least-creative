import json
import math
import os
from collections import defaultdict, Counter

en_dir = 'data/articles/en/'
de_dir = 'data/articles/de/'
bg_dir = 'data/articles/bg/'
def read_files_from_directory(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get all the file names from the directory
    files = [f for f in os.listdir(directory) if f.endswith('.json')]

    # Read the contents of each file
    file_contents = []
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            content = json.load(file)
            file_contents.append(content)

    return file_contents
def get_all_articles():
    en_files = read_files_from_directory(en_dir)
    de_files = read_files_from_directory(de_dir)
    bg_files = read_files_from_directory(bg_dir)

    # Combine all three lists into one array
    all_files = en_files + de_files + bg_files
    return de_files
# Sample articles data
articles = get_all_articles()

# Sample query
query = "The economy and market trends"

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

# Assuming query keywords are already extracted
query_keywords = ['economy', 'market', "inflation"]  # Replace with actual query keywords extraction
matching_article_ids = retrieve_articles(query_keywords)
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

ranked_article_ids = rank_articles(query_keywords, tf_idf_scores)
ranked_articles = [article for article_id, score in ranked_article_ids for article in articles if article['id'] == article_id]

# Step 5: Display Top-N Articles
top_n = 10  # Number of top articles to display
top_articles = ranked_articles[:top_n]

for article in top_articles:
    print(f"Title: {article['title']}")
    print(f"Content: {article['content'][:200]}...")  # Display first 200 characters of the content
    print("\n")
