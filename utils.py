import os
import glob


def list_text_files(directory):
    # Construct the pattern to match all .txt files
    pattern = os.path.join(directory, '*.txt')

    # Use glob to find all files matching the pattern
    text_files = glob.glob(pattern)

    return text_files

def save_to_file(data, file_name):
    """
    Saves a list of lists of tuples to a text file.

    Args:
    data (list of list of tuples): The data to be saved.
    file_name (str): The name of the file where the data will be saved.
    """
    # Extract directory from the file name
    directory = os.path.dirname(file_name)

    # If the directory does not exist, create it
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_name, 'w') as file:
        for sublist in data:
            # Convert each tuple in the sublist to a string and join them with commas
            line = ', '.join(str(tup) for tup in sublist)
            file.write(line + '\n')