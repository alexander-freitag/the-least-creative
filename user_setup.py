# Description: This file is used to setup the project.
# It is executed when the project is imported and should only be run once.
# It should be used to download all large files (e.g., model weights) and store them to disk.
# It checks if the environment works as expected.
# If something goes wrong, the script exits with a non-zero exit code.
# This helps detect issues early on.
import os
import sys

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from user_config import DE_MODEL_PATH, BG_MODEL_PATH


def download_large_files():
    de_model_path = DE_MODEL_PATH
    bg_model_path = BG_MODEL_PATH

    # Create directories if they do not exist
    os.makedirs(de_model_path, exist_ok=True)
    os.makedirs(bg_model_path, exist_ok=True)

    # Download German to English model and tokenizer
    model_de = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")
    tokenizer_de = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")

    # Save model and tokenizer
    model_de.save_pretrained(de_model_path)
    tokenizer_de.save_pretrained(de_model_path)

    # Download Bulgarian to English model and tokenizer
    model_bg = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-bg-en")
    tokenizer_bg = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-bg-en")

    # Save model and tokenizer
    model_bg.save_pretrained(bg_model_path)
    tokenizer_bg.save_pretrained(bg_model_path)
    return True


def check_environment():
    # Check Python version
    if sys.version_info < (3, 6):
        return False
    # Check if torch is available
    try:
        import torch
    except ImportError:
        return False

    # Check for GPU availability
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU.")
    else:
        print("CUDA is not available. Using CPU.")

    # Check if transformers is installed
    try:
        import transformers
    except ImportError:
        return False

    return True


if __name__ == "__main__":
    print("Perform your setup here.")

    if not check_environment():
        print("Environment check failed.")
        exit(1)

    if not download_large_files():
        print("Downloading large files failed.")
        exit(1)

    exit(0)
