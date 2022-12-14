"""
Contains the functions used to scrape data and convert between dictionaries and
CSVs.
"""
import csv
from string import punctuation
from collections import Counter
import praw
from api_keys import keys

# Creates a read-only instance of Reddit.
reddit = praw.Reddit(
    client_id=keys["CLIENT_ID"],
    client_secret=keys["CLIENT_SECRET"],
    password=keys["PASSWORD"],
    user_agent=keys["USERAGENT"],
    username=keys["USERNAME"],
)


def strings_to_subreddits(subreddit_strings):
    """
    Converts a given list of strings into a list of subreddit types.

    Args:
        subreddit_strings: A list of strings representing the names of subreddits
            to eventually collect data from.
    Returns:
        A list of subreddit objects corresponding to the given names.
    """
    subreddits = []
    for string in subreddit_strings:
        subreddits.append(reddit.subreddit(string))
    return subreddits




def scrape_subreddits(subreddit_strings, num_posts):
    """
    Scrapes the top submissions of a given list of subreddits for a given number
    of posts.

    Args:
        subreddit_strings: A list of strings representing the names of subreddits
            to collect data form.
        num_posts: The number of submissions to go through on each subreddit.
    Returns:
        A dictionary containing every word present in the subreddit's submissions,
        excluding capitalization and punctuation, and the number of times that
        word shows up.
    """
    subreddits = strings_to_subreddits(subreddit_strings)

    words = ""
    for subreddit in subreddits:
        for submission in subreddit.top(limit=num_posts):
            words += submission.selftext.lower().translate(str.maketrans('', '', punctuation))
    words = words.split()

    word_dict = (Counter(words))
    return word_dict


def csv_to_dict(file_name):
    """
    Given a file name, converts a CSV to a dictionary.

    Assumes that the CSV being converted is a frequency dictionary and as a result,
    casts all of the values to integers.

    Args:
        file_name: The path for the CSV file to convert to a dictionary.
    Returns:
        None.
    """
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        word_dict = {}
        for key, value in reader:
            word_dict[key] = int(value)
    return word_dict



def dict_to_csv(word_dict, file_name):
    """
    Given a dictionary and a file name, creates a new CSV containing the contents
    of the dictionary.

    Args:
        word_dict: A dicitonary to be converted into a CSV.
        file_name: The path for the CSV file the dictionary is being converted
            into.
    Return:
        None.
    """
    with open(file_name, 'w') as file:
        for key in word_dict.keys():
            file.write("%s,%s\n" % (key, word_dict[key]))
