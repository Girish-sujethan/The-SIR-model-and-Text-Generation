"""CSC110 Fall 2020 Assignment 3, Part 3: Loops and Mutation Debugging Exercise

Instructions (READ THIS FIRST!)
===============================

This Python module contains the program and tests described in Part 3.
Run this file to see the pytest report containing at least one failing test.

While you are making small changes to this file, we will NOT run python_ta
on this file when grading.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 David Liu and Mario Badr.
"""
import csv
import math
from typing import Dict, List, Tuple

# Constant for different punctuation marks to remove from review strings.
PUNCTUATION = '!\"#$%&()*+,-./:;<=>?@[]^_`{|}~'

# Constant representing VADER word intensities.
# (This is a small subset of the full VADER lexicon.)
WORD_TO_INTENSITY = {
    'adventure': 1.3,
    'amusing': 1.6,
    'brilliantly': 3.0,
    'comedy': 1.5,
    'excellent': 2.7,
    'guilty': -1.8,
    'magnificent': 2.9,
    'succeeded': 1.8,
    'terrible': -2.1
}


###############################################################################
# Mario's Program
###############################################################################
def report_sentiment(review: str) -> Tuple[str, float]:
    """Return the VADER sentiment of the review in text.

    The VADER sentiment is a tuple of the polarity, intensity of the review.
    """
    # First clean the review text and split into a list of words.
    word_list = clean_text(review)

    # Extract the number of times each VADER keyword appears in the review.
    occurrences = count_keywords(word_list)

    # Calculate the average intensity of the keywords in the review.
    average_intensity = calculate_average_intensity(occurrences)

    if average_intensity >= 0.05:
        return ('positive', average_intensity)
    elif average_intensity <= -0.05:
        return ('negative', average_intensity)
    else:
        return ('neutral', average_intensity)


def clean_text(text: str) -> List[str]:
    """Return text as a list of words that have been cleaned up.

    Cleaning up involves:
        - removing punctuation
        - converting all letters to lowercase (because our VADER keywords
          are all written as lowercase)
    """
    # Remove punctuation from text
    for p in PUNCTUATION:
        text = str.replace(text, p, ' ')

    # Convert text to lowercase
    text = str.lower(text)

    # Split text into words and return
    return str.split(text)


def count_keywords(word_list: List[str]) -> Dict[str, int]:
    """Return a frequency mapping of the VADER keywords in text.
    """
    # ACCUMULATOR: A mapping of keyword frequencies seen so far
    occurrences_so_far = {}

    for word in word_list:
        if word in WORD_TO_INTENSITY:
            if word not in occurrences_so_far:
                occurrences_so_far[word] = 0

            occurrences_so_far[word] = occurrences_so_far[word] + 1

    return occurrences_so_far


def calculate_average_intensity(occurrences: Dict[str, int]) -> float:
    """Return the average intensity of the given keyword occurrences.

    Preconditions:
        - occurrences != {}
        - all({occurrences[keyword] >= 1 for keyword in occurrences})
    """
    num_keywords = sum([occurrences[word] for word in occurrences])
    total_intensity = sum([WORD_TO_INTENSITY[word] * occurrences[word]
                           for word in occurrences])
    return total_intensity / num_keywords


###############################################################################
# Tests for report_sentiment (THERE ARE NO ERRORS IN THIS PART)
###############################################################################
def read_critic_data(filename: str) -> str:
    """Return the movie review stored in the given file.

    The file is a CSV file with two rows, a header row and a row of actual
    movie review data. These files are based on real movie review data from Metacritic,
    though they have been altered slightly to fit this assignment.

    There ARE NO ERRORS in this function; it's used for testing purposes only.
    """
    with open(filename) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        # Read the movie review, which is the last entry in the row
        row = next(reader)
        review = row[len(row) - 1]

    return review


def test_star_wars() -> None:
    """Test that the review for Star Wars gives the correct polarity and intensity.

    There is NO ERROR in this test.
    """
    review = read_critic_data('data/reviews/review_star_wars.csv')

    actual = report_sentiment(review)
    expected_polarity = 'positive'
    expected_intensity = 2.25
    assert actual[0] == expected_polarity
    assert math.isclose(actual[1], expected_intensity)


def test_legally_blonde() -> None:
    """Test that the review for Legally Blonde gives the correct polarity and intensity.

    There is NO ERROR in this test.
    """
    review = read_critic_data('data/reviews/review_legally_blonde.csv')

    actual = report_sentiment(review)
    expected_polarity = 'positive'
    expected_intensity = 0.8333333333333333
    assert actual[0] == expected_polarity
    assert math.isclose(actual[1], expected_intensity)


def test_transformers() -> None:
    """Test that the review for Transformers gives the correct polarity and intensity.

    There is NO ERROR in this test.
    """
    review = read_critic_data('data/reviews/review_transformers.csv')

    actual = report_sentiment(review)
    expected_polarity = 'negative'
    expected_intensity = -0.9
    assert actual[0] == expected_polarity
    assert math.isclose(actual[1], expected_intensity)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import pytest
    pytest.main(['a3_part3.py', '-v'])
