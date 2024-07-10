# Description: This script is used to preprocess the input data.
# It extracts the title, content, and timestamp from the input file.
# It detects the language of the content and translates it to English if needed.
# It also extracts keywords from the translated content.
# The output is saved in a JSON file in the output directory.

import json
import os
from os.path import join, split
from translation import translate_german_to_english, translate_bulgarian_to_english, detect_language
from keyword_extractor import extract_keywords

# This function is used to handle the input file
def handle_input_file(file_location, output_path):
    with open(file_location, encoding='utf-8') as f:
        data = json.load(f)

    # Extracting the title, content, and timestamp from the input file
    title = data["title"]
    content = data["content"]
    timestamp = data["timestamp"]

    # Detecting the language of the content
    detected_language = detect_language(content)
    
    # Translating the content to English if needed and extracting keywords
    if detected_language == "de":
        translation = translate_german_to_english(content)
        keywords = extract_keywords(translation)
    elif detected_language == "bg":
        translation = translate_bulgarian_to_english(content)
        keywords = extract_keywords(translation)
    elif detected_language == "en":
        translation = ""
        keywords = extract_keywords(content)
    else:
        raise ValueError("Language not supported or recognized")

    result = {
        "title": title,
        "timestamp": timestamp,
        "content": content,
        "keywords": keywords,
        "language": detected_language,
        "translation": translation
    }
    

    # Check if output path exists and create it if not
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_name = split(file_location)[-1]
    with open(join(output_path, file_name), "w", encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)

    # python user_preprocess.py --input article_test.json --output results
    

# The code below is used to parse the command line arguments
import argparse
parser = argparse.ArgumentParser(description='Preprocess the data.')
parser.add_argument('--input', type=str, help='Path to the input data.', required=True, action="append")
parser.add_argument('--output', type=str, help='Path to the output directory.', required=True)

if __name__ == "__main__":
    args = parser.parse_args()
    files_inputs = args.input
    files_out = args.output
    
    for file_location in files_inputs:
        handle_input_file(file_location, files_out)
