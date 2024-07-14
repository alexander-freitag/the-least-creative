# Description: This script is used to preprocess the input data.
# It extracts the title, content, and timestamp from the input file.
# It detects the language of the content and translates it to English if needed.
# It also extracts keywords from the translated content.
# The output is saved in a JSON file in the output directory.

import json
import argparse
import os

from translation import detect_language
from dataset import save_article, populate
from user_config import ARTICLES_DIR


# This function is used to handle the input file
def handle_input_file(file_location, output_dir=ARTICLES_DIR):
    with open(file_location, encoding='utf-8') as f:
        data = json.load(f)

    # Extracting the title, content, and timestamp from the input file
    title = data["title"]
    content = data["content"]
    timestamp = data["timestamp"]

    # Detecting the language of the content
    detected_language = detect_language(content)

    # Building the output path
    file_name = os.path.basename(file_location)

    # Create output dir if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, file_name + '.json')

    # Saving the output in a JSON file in the output directory
    save_article(title, timestamp, content, detected_language, output_path)
  

def create_dataset():
    populate()


# This is a useful argparse-setup, you probably want to use in your project:
parser = argparse.ArgumentParser(description='Preprocess the data.')
parser.add_argument('--input', type=str, help='Path to the input data.', action="append")
parser.add_argument('--output', type=str, help='Path to the output directory.', default=ARTICLES_DIR)

if __name__ == "__main__":
    args = parser.parse_args()
    files_inp = args.input
    files_out = args.output
    
    if files_inp is not None:
        if files_out is None:
            print("No output directory provided. Using default directory. These files will be added to the final dataset.")
            files_out = ARTICLES_DIR
        else:
            if not os.path.exists(files_out):
                os.makedirs(files_out)
            print("Output directory provided. These files will NOT be added to the final dataset.")
        for file_location in files_inp:
            handle_input_file(file_location, files_out)
    else:
        print("No input files provided.")

    create_dataset()
    print("Final dataset created. Data preprocessing completed.")
