import json
import os


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


def save_articles(title, timestamp, content, keywords, language):
    # Test if title is of type string
    if not isinstance(title, str):
        raise TypeError("Title must be a string.")
    
    # Test if timestamp is of type string
    if not isinstance(timestamp, str):
        raise TypeError("Timestamp must be a string.")
    
    # Test if content is of type string
    if not isinstance(content, str):
        raise TypeError("Content must be a string.")
    
    # Test if keywords is of type list
    if not isinstance(keywords, list):
        raise TypeError("Keywords must be a list.")
    
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
    elif language == 'bg':
        directory = bg_dir
    elif language == 'de':
        directory = de_dir
    else:
        raise ValueError("Language must be 'en', 'bg', or 'de'.")
    
    # Create the file path
    file_path = f'{directory}{new_id}.json'
    
    # Create the JSON data
    data = {
        'title': title,
        'timestamp': timestamp,
        'content': content,
        'keywords': keywords,
        'language': language
    }
    
    # Save the JSON data to the file
    with open(file_path, 'w') as file:
        json.dump(data, file)
    
    print("Article saved at:", file_path)

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


# def add_keywords(file_id, language, keywords):
#     # Get the article data
#     article_data = open_article(file_id, language)
    
#     # Check if the keywords are of type list
#     if not isinstance(keywords, list):
#         raise TypeError("Keywords must be a list.")
    
#     # Add the keywords to the article data
#     article_data['keywords'].extend(keywords)
    
#     # Create the file path
#     file_path = f'data/articles/{language}/{file_id}-{language}.json'
    
#     # Save the updated article data to the file
#     with open(file_path, 'w') as file:
#         json.dump(article_data, file)
        
#     return article_data['keywords']


# def get_articles_preformat(language):
#     # Get the list of article files in the specified language directory
#     directory = f'data/articles/{language}/'
#     files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
#     # Initialize an empty list to store the article data
#     articles = []
    
#     # Iterate over each file
#     for file in files:
#         # Extract the file id from the filename
#         file_id = int(file.split('-')[0])
        
#         # Create the file path
#         file_path = os.path.join(directory, file)
        
#         # Read the JSON data from the file
#         with open(file_path, 'r') as f:
#             data = json.load(f)
        
#         # Extract the keywords from the article data
#         keywords = data['keywords']
        
#         # Append the article id, keywords, and language to the list
#         articles.append({'id': file_id, 'language': language, 'keywords': keywords, })
    
#     return articles


# def get_all_articles():
#     # Initialize an empty list to store all articles
#     all_articles = []
    
#     # List of languages
#     languages = ['en', 'bg', 'de']
    
#     # Iterate over each language
#     for language in languages:
#         # Get articles with id and keywords for the language
#         articles = get_articles_preformat(language)
        
#         # Extend the all_articles list with articles for the language
#         all_articles.extend(articles)
    
#     return all_articles


# def format_articles(article):
#     return f"ID: {article['id']}; Language: {article['language']}; Keywords: {', '.join(article['keywords'])}"


# def format_all_articles():
#     all_articles = get_all_articles()
#     formatted_articles = [format_articles(article) for article in all_articles]
#     return '\n'.join(formatted_articles)

