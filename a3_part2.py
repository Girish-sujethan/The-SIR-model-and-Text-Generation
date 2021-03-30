"""CSC110 Fall 2020 Assignment 3, Part 2: Text Generation, One-Word Context Model

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
from typing import Dict, Set


###############################################################################
# Question 2
###############################################################################
def create_model_owc(text: str) -> Dict[str, Set[str]]:
    """Return the one-word context model of the given text.

    Your implementation MUST use the update_follow_set helper function (see below).
    We recommend completing that function first, as it's simpler and will give you
    thinking about how to use it here.

    A "word" here consists only of alphanumeric characters (no spaces).

    Preconditions:
        - text != ''
        - all({str.isalnum(c) or c in {' ', '.'} for c in text})
        - any({str.isalnum(c) for c in text})
        - Each period in text is immediately preceded by a word and immediately
          followed by a space.

    HINTS:
        - A good starting point is to split the text using str.split.
        - Each word might have a period at the end; the ones with a period need
          to be handled differently. You can use *string slicing* to obtain a part
          of a string, e.g.

            >>> s = 'word.'
            >>> s[0:4]  # The part of s from indexes 0 to 3 inclusive
            'word'
            >>> s[0:-1]  # Can also use a negative index to mean "count from the end"
            'word'

        - You can use an *index-based loop* to keep track of pairs of adjacent words.
        - Another useful str method might be str.rstrip. Note that str.removesuffix
          is NOT allowed, since it's only available in a newer version of Python
          than the one we're using in this course.

        asdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        create_model_owc('Love is patient. Love is kind. It does not envy. It does not boast. It is not proud.')
        create_model_owc('I like chocolate. I really really like chocolate.')
        print(str(x+1)+" & "+list_of_words[x]+" & "+list_of_words[x+1]+ " & "+ str(dict_so_far))
    """
    dict_so_far = {}
    list_of_words = str.split(text)


    for x in range(0, len(list_of_words)):
        """
        check if the word is followed by a period and add it to the follow list if it is, then remove the period to 
        check if the word is followed by something else
        """
        if list_of_words[x][-1] == '.':
            list_of_words[x] = list_of_words[x][0:-1]
            update_follow_set(dict_so_far, list_of_words[x], '.')

        else:
            update_follow_set(dict_so_far, list_of_words[x], list_of_words[x + 1].rstrip('.'))
    return dict_so_far


def update_follow_set(model: Dict[str, Set[str]], word: str, follow_word: str) -> None:
    """Mutate model by adding follow_word to the follow set of word.

    If word is not already present in the model, add it to the model with follow set {follow_word}.

    >>> my_model = {}
    >>> update_follow_set(my_model, 'I', 'like')
    >>> my_model == {'I': {'like'}}
    True
    >>> update_follow_set(my_model, 'I', 'really')
    >>> my_model == {'I': {'like', 'really'}}
    True
    """
    if word not in model:
        model[word] = {follow_word}

    else:
        model[word].add(follow_word)


###############################################################################
# Question 3
###############################################################################
def generate_text_owc(model: Dict[str, Set[str]], n: int) -> str:
    """Return a string containing n randomly generated words chosen from model.

    Your implementation MUST use the generate_new_word and generate_next_word helper functions.
    We recommend completing those functions first, as they're simpler and will give you
    thinking about how to use them here.

    Preconditions:
        - n > 0
        - model is in the format described by the assignment handout
    """
    # ACCUMULATOR: a list of the randomly-generated words so far
    words_so_far = []
    # We've provided this template as a starting point; you may modify it as necessary.
    words_so_far.append(generate_new_word(model))
    for x in range(0, n-1):
        key = words_so_far[x]
        new_word = generate_next_word(model,key)
        if new_word == ".":
            words_so_far[x] = words_so_far[x]+'.'
            new_word= generate_new_word(model)
        elif new_word == {}:
            new_word = generate_new_word(model)
        words_so_far.append(new_word)

    return str.join(' ', words_so_far)


def generate_new_word(model: Dict[str, Set[str]]) -> str:
    """Return a randomly generated word from the given model.

    Choose the word randomly from all keys in model.

    You can turn the keys of a dictionary my_dict into a list using list(dict.keys(my_dict)).

    Preconditions:
        - model != {}
        - model is in the format described by the assignment handout
    """
    all_keys = list(dict.keys(model))
    return random.choice(all_keys)


def generate_next_word(model: Dict[str, Set[str]], word: str) -> str:
    """Return a randomly generated word from the follow set of the given word.

    Preconditions:
        - model is in the format described by the assignment handout
        - word in model
        - model[word] != set()
    """
    possible_words = [pos_word for pos_word in model[word]]
    return random.choice(possible_words)


def load_text_data(filepath: str) -> str:
    """Read and return the text from from the given filepath.

    You are free to use/modify this function however you like;
    we have provided it to you for testing purposes only.

    Note for the assignment: the text file we've provided is in
    'data/texts/sample_text_clean.txt'.
    """
    with open(filepath) as text_file:
        text_from_file = text_file.read()

    return str.strip(text_from_file)  # str.strip removes leading/trailing whitespace


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-io': ['load_text_data'],
    #     'extra-imports': ['python_ta.contracts', 'random'],
    #     'max-line-length': 100,
    #     'disable': ['R1705'],
    #     'max-nested-blocks': 4
    # })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
