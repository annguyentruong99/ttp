import os
import glob


def list_text_files(directory):
    # Construct the pattern to match all .txt files
    pattern = os.path.join(directory, '*.txt')

    # Use glob to find all files matching the pattern
    text_files = glob.glob(pattern)

    return text_files