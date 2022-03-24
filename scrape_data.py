
import praw
import csv
from string import punctuation
from collections import Counter
from api_keys import keys


def strings_to_subreddits(subreddit_strings):
    subreddits = []
    for string in subreddit_strings:
        subreddits.append(reddit.subreddit(string))
    return subreddits

def scrape_subreddits(subreddit_strings, num_posts):
    subreddits = strings_to_subreddits(subreddit_strings)

    words = ""

    for subreddit in subreddits:
        for submission in subreddit.top(limit=num_posts):
            words += submission.selftext.lower().translate(str.maketrans('', '', punctuation))
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            words += comment.body.lower().translate(str.maketrans('', '', punctuation))
    words = words.split()

    word_dict = (Counter(words))
    return word_dict

def dict_to_csv(word_dict, file_name):
    with open(file_name, 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in word_dict.items():
            writer.writerow([key, value])

def csv_to_dict(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        word_dict = dict(reader)
    return word_dict