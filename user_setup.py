# Description: This file is used to setup the project.
# It is executed when the project is imported and should only be run once.
# It should be used to download all large files (e.g., model weights) and store them to disk.
# It checks if the environment works as expected.
# If something goes wrong, the script exits with a non-zero exit code.
# This helps detect issues early on.

def download_large_files():
    return True

def check_environment():
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