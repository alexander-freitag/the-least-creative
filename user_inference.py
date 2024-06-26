# This file will be executed when a user wants to query your project.
# This file will be executed when a user wants to query your project.
import argparse
from os.path import join
import json
import requests as r
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the tokenizer
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")


# Function to load and preprocess the dataset
def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    articles = data["articles"]
    return articles


def handle_user_query(query, query_id, output_path):
    call_data = {
        "model": "llama3",
        "prompt": "User Query: " + query,
        "system": "You are a helpful assistant working at the EU. It is your job to give users unbiased article recommendations. You will be prompted with a user generated search query. Try to improve it by adding more context, such that a recommendation system has an easier time to find relevant articles. Response with the improved query only. The query should be unbiased and in English. The query is given as the next message. Only answer with the improved query. After the query, append LANGUAGE: [lang_code] where you use the default two-letter language code in a new line.",
        "stream": False
    }
    response = r.post("http://localhost:11434/api/generate", json=call_data)
    response = response.json()
    response_text = response["response"]

    new_query, language_code = response_text.split("LANGUAGE: ")
    new_query = new_query.strip()
    language_code = language_code.strip()

    result = {
        "generated_queries": [new_query],
        "detected_language": language_code,
    }

    print(response_text)

    with open(join(output_path, f"{query_id}.json"), "w") as f:
        json.dump(result, f)

    # Extract keywords from the query
    keywords = extract_keywords(new_query)

    # Load dataset and rank articles
    articles = load_dataset('dataset.json')
    ranked_articles = rank_articles(keywords, articles)

    # Save the results
    with open(join(output_path, f"{query_id}_results.json"), "w") as f:
        json.dump(ranked_articles, f)


def extract_keywords(query):
    # Simple keyword extraction using tokenization
    tokens = tokenizer.tokenize(query)
    return " ".join(tokens)


def rank_articles(generated_queries, article_representations):
    """
    This function takes as arguments the generated / augmented user query, as well as the
    transformed article representations.

    It needs to return a list of shape (M, 2), where M <= #article_representations.
    Each tuple contains [index, score], where index is the index in the article_repr array.
    The list need already be ordered by score. Higher is better, between 0 and 1.

    An empty return list indicates no matches.
    """

    system_prompt = """You are a helpful assistant working at the EU. It is your job to give users unbiased article recommendations. You will be given a user query, and a list of articles. Your task is to rank the articles by relevance to the query. Response with a list of article indices and rankings as nested JSON arrays. The first index should be the most relevant article, the last the least relevant. The indices should be 0-based. The rankings should be "VERY", "HIGH", "MEDIUM", or "IRRELEVANT". If there are multiple queries, it is only variations of one original one. Only return the rankings as valid JSON, for example [[3, "HIGH"], [5, "MEDIUM"]]. Do not give me anything else, nor any explanation."""

    article_string = [f"Article {index}: {json.dumps(article)}" for index, article in
                      enumerate(article_representations)]
    user_prompt = "User Query: " + json.dumps(generated_queries) + "\n\n" + "Articles: " + "\n".join(article_string)

    # This call is using the raw mode (raw=True). This mode gives you more flexibility in the response, but is a bit more complex.
    # You need to look up the template file of your model and format the request accordingly.
    # If you use raw, other parameters, in particular system, have no effect, as raw overrides them.
    #
    # The key advantage of the raw mode is that you can force the model to start with a specific string.
    # In the example below, we start the model response with "[[", which strongly conditions the model to output JSON.
    call_data = {
        "model": "llama3",
        "stream": False,
        "raw": True,
        "prompt": f"""system

        {system_prompt}user

        {user_prompt}assistant[["""
    }

    response = r.post("http://localhost:11434/api/generate", json=call_data)
    response = response.json()

    # The model will not regenerate "[[", so we need to add it back in.
    response = json.loads('[[' + response["response"])

    def s2i(score):
        if score == "VERY": return 1.0
        if score == "HIGH": return 0.75
        if score == "MEDIUM": return 0.5
        return 0.0

    response = [[index, s2i(score)] for index, score in response]
    return response


if __name__ == "__main__":
    # This is a sample argparse-setup, you probably want to use in your project:
    parser = argparse.ArgumentParser(description='Run the inference.')
    parser.add_argument('--query', type=str, help='The user query.', required=True, action="append")
    parser.add_argument('--query_id', type=str, help='The IDs for the queries, in the same order as the queries.',
                        required=True, action="append")
    parser.add_argument('--output', type=str, help='Path to the output directory.', required=True)

    args = parser.parse_args()
    queries = args.query
    query_ids = args.query_id
    output = args.output

    assert len(queries) == len(query_ids), "The number of queries and query IDs must be the same."

    for query, query_id in zip(queries, query_ids):
        handle_user_query(query, query_id, output)