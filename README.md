**Please adjust ```user_config.py``` to your needs before starting.**

1. ```python user_setup.py```.
    - Checks if all dependencies in ```requirements.txt``` are present.
    - Downloads Helsinki-NLP.
    - Checks if Ollama responds.

2. ```python user_preprocess.py```. 
    - Without arguments: From all of the preprocessed article files in ```ARTICLES_DIR``` creates a single JSON final dataset file in ```DATASET_PATH```.
    - Using --input: Processes input article files and adds them to ```ARTICLES_DIR```. Then creates the final dataset in ```DATASET_PATH```, including them.
    - Using --input and --output: Processes input article files and writes them to the given output path. These articles are NOT INCLUDED in the final dataset for comparison.
    
3. ```python user_inference.py -user_query "[USER QUERY]" -output_file "[OUTPUT_FILE]"```.
    - If the --output is not given, result will be saved to ```QUERIES_PATH```.
