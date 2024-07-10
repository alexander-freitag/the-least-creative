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
from handle_articles import save_article

# This function is used to handle the input file
def handle_input_file(file_location):
    with open(file_location, encoding='utf-8') as f:
        data = json.load(f)

    # Extracting the title, content, and timestamp from the input file
    title = data["title"]
    content = data["content"]
    timestamp = data["timestamp"]

    # Detecting the language of the content
    detected_language = detect_language(content)

    # Saving the output in a JSON file in the output directory
    save_article(title, timestamp, content, detected_language)
  

# The code below is used to parse the command line arguments
import argparse
parser = argparse.ArgumentParser(description='Preprocess the data.')
parser.add_argument('--input', type=str, help='Path to the input data.', required=True, action="append")

if __name__ == "__main__":
    args = parser.parse_args()
    files_inputs = args.input
    files_out = args.output
    
    for file_location in files_inputs:
        handle_input_file(file_location)
