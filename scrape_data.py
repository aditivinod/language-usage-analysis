
import praw
import csv
from string import punctuation
from collections import Counter
from api_keys import keys
import pandas as pd

"""
Creates an instance of a reddit 
"""
reddit = praw.Reddit(
    client_id = keys["CLIENT_ID"],
    client_secret = keys["CLIENT_SECRET"],
    password = keys["PASSWORD"],
    user_agent = keys["USERAGENT"],
    username = keys["USERNAME"],
)

"""
Do the docstring, bitch.
"""
def strings_to_subreddits(subreddit_strings):
    subreddits = []
    for string in subreddit_strings:
        subreddits.append(reddit.subreddit(string))
    return subreddits

"""
Do the docstring, bitch.
"""
def scrape_subreddits(subreddit_strings, num_posts):
    subreddits = strings_to_subreddits(subreddit_strings)

    words = ""
    for subreddit in subreddits:
        for submission in subreddit.top(limit=num_posts):
            words += submission.selftext.lower().translate(str.maketrans('', '', punctuation))
            # submission.comments.replace_more(limit=None)
            # for comment in submission.comments:
                # words += comment.body.lower().translate(str.maketrans('', '', punctuation))
    words = words.split()

    word_dict = (Counter(words))
    return word_dict

"""
Do the docstring, bitch.
"""
def csv_to_dict(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        word_dict = {}
        for key, value in reader:
            word_dict[key] = int(value)
    return word_dict

"""
Do the docstring, bitch.
"""
def dict_to_csv(word_dict, file_name):
    with open(file_name, 'w') as f:
        for key in word_dict.keys():
            f.write("%s,%s\n" % (key, word_dict[key]))

"""
Do the docstring, bitch.
"""
def scrape_user(username): # dysfunctional rn
    #username = reddit.subreddit("r/u_" + username)
    print("F")
    redditor = reddit.redditor(username)

    words = ""
    for submission in redditor.submissions.new(limit=None):
        words += submission.selftext.lower().translate(str.maketrans('', '', punctuation))
    # submission.comments.replace_more(limit=None)
    # for comment in submission.comments.list():
            # words += comment.body.lower().translate(str.maketrans('', '', punctuation))
    words = words.split()

    word_dict = (Counter(words))
    return word_dict