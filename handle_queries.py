import json
import os


# Define the directory
queries_dir = 'data/queries/'


def get_last_query():
    # Check if the directory exists and create it if not
    if not os.path.exists(queries_dir):
        os.makedirs(queries_dir)
        return 0

    # List all files in the directory
    files = [f for f in os.listdir(queries_dir) if f.endswith('.json')]
    
    # Sort files based on the numeric part of the filename
    files.sort(key=lambda x: int(x.split('.')[0]))
    
    # Return the last query id in the sorted list
    if files:
        # Get ids from the filenames
        id = int(files[-1].split('.')[0])
        return id
    else:
        return 0
    
    
def save_query(query, timestamp, detected_keywords, detected_language, rank_articles):
    # Test if query is of type string
    if not isinstance(query, str):
        raise TypeError("Query must be a string.")
    
    # Test if timestamp is of type string
    if not isinstance(timestamp, str):
        raise TypeError("Timestamp must be a string.")
    
    # Test if detected_keywords is of type list
    if not isinstance(detected_keywords, list):
        raise TypeError("Detected keywords must be a list.")
    
    # Test if detected_language is valid
    if detected_language not in ['en', 'bg', 'de']:
        raise ValueError("Detected language must be 'en', 'bg', or 'de'.")
    
    # Test if rank_articles is of type list
    if not isinstance(rank_articles, list):
        raise TypeError("Detected keywords must be a list.")
    
    # Get the last query id
    last_id = get_last_query()

    # Increment the id
    new_id = last_id + 1

    # Create the file path
    file_path = f'{queries_dir}{new_id}.json'
    
    # Create the JSON data
    data = {
        'query': query,
        'timestamp': timestamp,
        'detected_keywords': detected_keywords,
        'detected_language': detected_language,
        'rank_articles': rank_articles
    }
    
    # Save the JSON data to the file
    with open(file_path, 'w') as file:
        json.dump(data, file)
        
    return new_id


def get_query(query_id):
    # Create the file path
    file_path = f'{queries_dir}{query_id}.json'
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Query with id {query_id} does not exist.")
    
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data


# # Example usage of get_last_query
# last_query_id = get_last_query()
# print(f"The last query id is: {last_query_id}")

# # Example usage of save_query
# query = "How to use Python?"
# timestamp = "2022-01-01 12:00:00"
# detected_keywords = ["Python", "programming"]
# detected_language = "en"
# rank_articles = ["article1", "article2", "article3"]
# new_query_id = save_query(query, timestamp, detected_keywords, detected_language, rank_articles)
# print(f"The new query id is: {new_query_id}")

# # Example usage of open_query
# query_id = 1
# query_data = get_query(query_id)
# print(f"The data for query id {query_id} is: {query_data}")