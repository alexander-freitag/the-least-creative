import os
import json
import uuid

from keyword_extractor import extract_keywords
from translation import translate_bulgarian_to_english, translate_german_to_english
from user_config import DATASET_PATH, ARTICLES_DIR


# Function to process a new article and create a dictionary with its data
def process_article(title, timestamp, content, language):
    # Check if the language is supported
    if language == "de":
        translation = translate_german_to_english(content)
        keywords = extract_keywords(translation)
    elif language == "bg":
        translation = translate_bulgarian_to_english(content)
        keywords = extract_keywords(translation)
    elif language == "en":
        translation = ""
        keywords = extract_keywords(content)
    else:
        raise ValueError("Language not supported or recognized")

    # Creates the dictionary with the article data
    data = {
        'timestamp': timestamp,
        'title': title,
        'content': content,
        'detected_language': language,
        'translation': translation,
        'transformed_representation': keywords
    }
    return data


# Function to save an article to a separate JSON file
def save_article(title, timestamp, content, language, file_path):
    # Process the article data and add a unique ID
    data = process_article(title, timestamp, content, language)
    data['id'] = str(uuid.uuid4())

    # Check if the directory exists and create it if not
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the article to the separate JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Function to check if a dataset exists
def dataset_exists(file_path=DATASET_PATH):
    return os.path.exists(file_path)


# Function to save the JSON dataset
def save_dataset(dataset, file_path=DATASET_PATH):
    # Check if the dataset directory exists and create it if not
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the dataset to the JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dataset, file, indent=4, ensure_ascii=False)


# Function to setup or clear the dataset file
def clear_dataset(file_path=DATASET_PATH):
    save_dataset([], file_path)


# Function to load the JSON dataset
def load_dataset(file_path=DATASET_PATH):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError("Dataset file does not exist")


# Function to add an article to the final dataset
def add_article(entry, dataset_path=DATASET_PATH):
    # Check if the entry has the required structure
    if 'timestamp' not in entry or \
       'title' not in entry or \
       'content' not in entry or \
       'detected_language' not in entry or \
       'translation' not in entry or \
       'transformed_representation' not in entry:
        raise ValueError("Entry does not have the required structure")
    
    # Generate a unique ID for the entry if it does not have one
    if 'id' not in entry:
        entry['id'] = str(uuid.uuid4())

    # Check and load the dataset if it exists
    if dataset_exists(dataset_path):
        dataset = load_dataset(dataset_path)
    else:
        dataset = []
    
    # Check if the ID already exists in the dataset. If it does, generate a new ID
    while entry['id'] in [data['id'] for data in dataset]:
        entry['id'] = str(uuid.uuid4())

    # Append the new entry to the dataset
    dataset.append(entry)

    # Save the dataset with the new entry
    save_dataset(dataset, dataset_path)
    return entry['id']


# Function to get an article by its ID from the final dataset
def get_article(article_id, file_path=DATASET_PATH):
    # Check and load the dataset if it exists
    dataset = load_dataset(file_path)

    # Find and return the article with the given ID
    for entry in dataset:
        if entry['id'] == article_id:
            return entry
    
    # Return None if the article was not found
    return None


# Function to delete an article by its ID from the final dataset
def delete_article(article_id, file_path=DATASET_PATH):
    # Check and load the dataset if it exists
    dataset = load_dataset(file_path)

    # Remove the article with the given ID from the dataset
    dataset = [entry for entry in dataset if entry['id'] != article_id]

    # Save the updated dataset
    save_dataset(dataset, file_path)

    # Return True if the article was deleted, False otherwise
    return get_article(article_id, file_path) is None


# Function to populate the final dataset with articles from the articles directory
def populate(articles_dir=ARTICLES_DIR, dataset_path=DATASET_PATH):
    # Return if the articles directory does not exist
    if not os.path.exists(ARTICLES_DIR):
        raise FileNotFoundError("Articles directory does not exist")
    
    # Setup the dataset file if it does not exist
    clear_dataset(dataset_path)

    # Get the list of JSON files in the directory
    json_files = [file for file in os.listdir(articles_dir) if file.endswith('.json')]

    # Iterate over each JSON file
    for file_name in json_files:
        file_path = os.path.join(articles_dir, file_name)

        # Load the JSON data from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        # Add the JSON data to the dataset
        add_article(json_data, dataset_path)