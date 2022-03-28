
import praw
import csv
from string import punctuation
from collections import Counter
from api_keys import keys
import pandas as pd

reddit = praw.Reddit(
    client_id = keys["CLIENT_ID"],
    client_secret = keys["CLIENT_SECRET"],
    password = keys["PASSWORD"],
    user_agent = keys["USERAGENT"],
    username = keys["USERNAME"],
)

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
            # submission.comments.replace_more(limit=None)
            # for comment in submission.comments:
                # words += comment.body.lower().translate(str.maketrans('', '', punctuation))
    words = words.split()

    word_dict = (Counter(words))
    return word_dict

def dict_to_csv(word_dict, file_name):
    pd.DataFrame.from_dict(data=word_dict, orient='index') \
        .to_csv('file_name', header=False)
   
def scrape_user(username):
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