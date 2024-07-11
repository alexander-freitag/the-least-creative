import json
import os

from keyword_extractor import extract_keywords
from translation import translate_bulgarian_to_english, translate_german_to_english


# Define the directories
en_dir = 'data/articles/en/'
de_dir = 'data/articles/de/'
bg_dir = 'data/articles/bg/'


def get_last_article():
    # Check if the directories exist and create them if not
    if not os.path.exists(en_dir):
        os.makedirs(en_dir)
    if not os.path.exists(de_dir):
        os.makedirs(de_dir)
    if not os.path.exists(bg_dir):
        os.makedirs(bg_dir)

    # Get all the file names from the directories that are json
    en_files = [f for f in os.listdir(en_dir) if f.endswith('.json')]
    bg_files = [f for f in os.listdir(bg_dir) if f.endswith('.json')]
    de_files = [f for f in os.listdir(de_dir) if f.endswith('.json')]

    # Combine all three lists into one array
    files = en_files + bg_files + de_files

    # Sort files based on the numeric part of the filename
    files.sort(key=lambda x: int(x.split('.')[0]))

    # Return the last query id in the sorted list
    if files:
        # Get ids from the filenames
        id = int(files[-1].split('.')[0])
        return id
    else:
        return 0


def save_article(title, timestamp, content, language):
    # Test if title is of type string
    if not isinstance(title, str):
        raise TypeError("Title must be a string.")

    # Test if timestamp is of type string
    if not isinstance(timestamp, str):
        raise TypeError("Timestamp must be a string.")

    # Test if content is of type string
    if not isinstance(content, str):
        raise TypeError("Content must be a string.")

    # Test if language is valid
    if language not in ['en', 'bg', 'de']:
        raise ValueError("Language must be 'en', 'bg', or 'de'.")

    # Get the last id
    last_id = get_last_article()

    # Increment the id
    new_id = last_id + 1

    # Choose the directory based on the language
    if language == 'en':
        directory = en_dir
        translation = content
    elif language == 'bg':
        directory = bg_dir
        translation = translate_bulgarian_to_english(content)
    elif language == 'de':
        directory = de_dir
        translation = translate_german_to_english(content)
    else:
        raise ValueError("Language must be 'en', 'bg', or 'de'.")

    # Create the file path
    file_path = f'{directory}{new_id}.json'

    # Extract keywords from the content 
    keywords = extract_keywords(translation)

    # Create the JSON data
    data = {
        'id': new_id,
        'title': title,
        'timestamp': timestamp,
        'content': content,
        'keywords': keywords,
        'language': language,
        'translation': translation
    }

    # Save the JSON data to the file with utf-8 encoding
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    return new_id


def get_article(file_id):
    # Check if the directories exist and create them if not
    if not os.path.exists(en_dir):
        os.makedirs(en_dir)
    if not os.path.exists(de_dir):
        os.makedirs(de_dir)
    if not os.path.exists(bg_dir):
        os.makedirs(bg_dir)

    file_name = f'{file_id}.json'

    # Choose the directory based on the language
    if file_name in os.listdir(en_dir):
        directory = en_dir
    elif file_name in os.listdir(de_dir):
        directory = de_dir
    elif file_name in os.listdir(bg_dir):
        directory = bg_dir
    else:
        error_str = f'Article with id {file_id} does not exist.'
        raise FileNotFoundError(error_str)

    # Create the file path
    file_path = f'{directory}{file_id}.json'

    if os.path.exists(file_path):
        # Read the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

        return data


def is_keywords_empty(file_id):
    # Get the article data
    article_data = get_article(file_id)

    # Check if the keywords list is empty
    if len(article_data['keywords']) == 0:
        return True
    else:
        return False


def get_keywords(file_id):
    # Get the article data
    article_data = get_article(file_id)

    # Return the keywords
    return article_data['keywords']


def add_keywords(file_id, keywords):
    # Get the article data
    article_data = get_article(file_id)

    # Check if the keywords are of type list
    if not isinstance(keywords, list):
        raise TypeError("Keywords must be a list.")

    # Add the keywords to the article data
    article_data['keywords'].extend(keywords)

    # Create the file path
    file_path = f'{article_data["language"]}{file_id}.json'

    # Save the updated article data to the file
    with open(file_path, 'w') as file:
        json.dump(article_data, file)

    return article_data['keywords']


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


def extract_ids_and_keywords(list_of_articles):
    extracted_data = []
    for article in list_of_articles:
        article_data = {
            'id': int(article['id']),
            'keywords': article['keywords']
        }
        extracted_data.append(article_data)
    return extracted_data


def format_articles(list_of_articles):
    formatted_articles = []
    for article in list_of_articles:
        article_id = article['id']
        keywords = ', '.join(article['keywords'])
        formatted_article = f"{article_id} ; {keywords}"
        formatted_articles.append(formatted_article)
    return formatted_articles


def format_all_articles():
    # Get all the articles from the directories
    en_files = read_files_from_directory(en_dir)
    de_files = read_files_from_directory(de_dir)
    bg_files = read_files_from_directory(bg_dir)

    # Combine all three lists into one array
    all_files = en_files + de_files + bg_files

    # Extract the ids and keywords from the articles
    extracted_data = extract_ids_and_keywords(all_files)

    # Format the articles
    formatted_articles = format_articles(extracted_data)

    return formatted_articles


def get_all_articles():
    en_files = read_files_from_directory(en_dir)
    de_files = read_files_from_directory(de_dir)
    bg_files = read_files_from_directory(bg_dir)

    # Combine all three lists into one array
    all_files = en_files + de_files + bg_files
    return all_files