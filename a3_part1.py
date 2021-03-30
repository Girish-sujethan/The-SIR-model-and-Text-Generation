"""CSC110 Fall 2020 Assignment 3, Part 1: Text Generation, Uniformly Random Model

Instructions (READ THIS FIRST!)
===============================
Implement each of the functions in this file. As usual, do not change any function headers
or preconditions. You do NOT need to add doctests.

You may create some additional helper functions to help break up your code into smaller parts.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 David Liu and Mario Badr.
"""
import random
from typing import List


def generate_text_uniform(model: List[str], n: int) -> str:
    """Return a string of n randomly-generated words chosen from the given model.

    Each word in the returned string is separated by a single space.

    Preconditions:
        - n >= 0
        - model != []
        - all({str.isalnum(s) for s in model})

    IMPLEMENTATION NOTE: Use the random.choice function to choose a random word from model.
    (Experiment with this function in the Python console.)

    >>> generate_text_uniform(['goodbye'], 3) -> str:
    'goodbye goodbye goodbye'
    """
    # ACCUMULATOR: a list of the randomly-generated words so far
    words_so_far = []

    for _ in range(0, n):
        # Complete the following statement to choose a random word from model.
        random_word = random.choice(model)
        list.append(words_so_far, random_word)

    return str.join(' ', words_so_far)


def create_model_uniform(text: str) -> List[str]:
    """Return a list of the words in the given text.

    This function should return model that is valid input to generate_text_uniform.
    A "word" here consists only of alphanumeric characters (no spaces).

    Preconditions:
        - text != ''
        - all({str.isalnum(c) or c == ' ' for c in text})
        - any({str.isalnum(c) for c in text})

    IMPLEMENTATION NOTE: Use the str.split method.
    """
    return str.split(text)


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['python_ta.contracts', 'random'],
    #     'max-line-length': 100,
    #     'disable': ['R1705']
    # })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
