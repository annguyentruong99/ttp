import numpy as np


def contains_duplicates(array: np.ndarray) -> bool:
    """
    Check if a numpy array contains any duplicates.

    :param array: Numpy array to check for duplicates.
    :return: True if there are duplicates, False otherwise.
    """
    # Convert the array to a set and compare its length to the array's length
    return len(np.unique(array)) != len(array)


def find_duplicate_indexes(array: np.ndarray):
    """
    Find the indexes of a duplicated number in a numpy array.

    :param array: Numpy array to check for a duplicated number.
    :return: The indexes of the duplicated number as two separate numbers.
    """
    seen = {}
    for index, element in enumerate(array):
        if element in seen:
            return seen[element], index
        seen[element] = index
    return None, None
