#take a dictionary of words and their relative frequency and parse through the
#data to find specific "gamer words"

example_dict = {"gamer":1, "gamers":2, "gaming":3, "the": 7, "potassium": 9, \
"potassiums" : 9
}

from operator import itemgetter
import math


def find_most_frequent(word_dictionary, number_items):
    """
    Find a specified number of keys from a dictionary that have the highest
    integer values

    Args:
        word_dictionary: a dictionary with strings as keys and positive
        integers as values
    Returns:
        most_frequent_dictionary: a dictionary with strings as keys and integers
        as values
    
    """
    most_frequent_dictionary = dict(sorted(word_dictionary.items(), key = \
        itemgetter(1), reverse = True)[:number_items])
    
    return most_frequent_dictionary



def instances_to_decimal(dictionary):
    """
    Convert the values of a dictionary from an integer to a decimal percentage
    of what percentage of the time that word is used in the total dataset

    Args:
        dictionary: a dictionary with strings as keys and positive integers
        as values
    Returns:
        dictionary: a dictionary with strings as keys and floats as values
    """
    total_words = sum(dictionary.values())
    for word in dictionary:
        dictionary[word] = dictionary[word]/total_words
    return dictionary

def remove_most_common(normal_dictionary, gamer_dictionary):
    """
    Remove words between dictionaries that show up similarly frequently

    Args:
        normal_dictionary = a dictionary with words as keys and integers as
        values, sorted from highest to lowest by value magnitude
        gamer_dictionary = a dictionary with words as keys and integers as
        values, sorted from highest to lowest by value magnitude
    
    Returns:
        normal_freq_dictionary = curated frequency list of normal words
        gamer_freq_dictionary = curated frequency list of gamer words
        ignore_list = a list of strings containing words which were omitted
            from both dictionaries
        
    """
    #convert values from the number of times a word is used to the frequency
    #of times the word is used total for both the normal and gamer dictionaries
    """
    normal_total_words = sum(normal_dictionary.values())
    for word in normal_dictionary:
        normal_dictionary[word] = normal_dictionary[word]/normal_total_words
    
    gamer_total_words = sum(gamer_dictionary.values())
    for word in gamer_dictionary:
        gamer_dictionary[word] = gamer_dictionary[word]/gamer_total_words
    """
    #normal_dictionary = instances_to_decimal(normal_dictionary)
    #gamer_dictionary = instances_to_decimal(gamer_dictionary)

    ignore_list = []
    for word in normal_dictionary:

        if word in gamer_dictionary and normal_dictionary[word]*1.15 > \
            gamer_dictionary[word] > normal_dictionary[word]*.85:

            ignore_list.append(word)
            gamer_dictionary.pop(word)
        
    for word in ignore_list:
        normal_dictionary.pop(word)
    
    return normal_dictionary,gamer_dictionary, ignore_list

def remove_too_uncommon(word_dictionary, threshold =20):
    """
    remove words from the dictionary that show up less than a specified
    number of times

    Args:
        word_dictionary: a dictionary with words as keys and integers as values
        threshold: an integer determining the minimum number of usages for a 
            word to be considered in the dictionary
    
    """

    delete_word = [key for key in word_dictionary if int(word_dictionary[key]) \
        < threshold]
    
    for key in delete_word: word_dictionary.pop(key)

    return word_dictionary

def determine_gamer_words(normal_dictionary,gamer_dictionary):

    """
    
    Args:
        gamer_dictionary: a dictionary with strings as keys and floats as the
            values representing what percentage of the time that string gets 
            used in the dataset
        normal_dictionary: a dictionary with strings as keys and floats as the
            values representing what percentage of the time that string gets 
            used in the dataset
    
    Returns:
        gamer_words: a list of strings representing words specific to the
        gamer vocabulary
    """
    gamer_words = []

    for word in gamer_dictionary:
        #determine a word to be a gamer word if it is used 50 times more
        #frequently in gamer subreddits than normal subreddits
        if word in normal_dictionary and normal_dictionary[word] <\
            gamer_dictionary[word]/5:
            gamer_words.append(word)
        #if the word is not present in the normal dictionary, then use a simple
        #percentage of uses comparison to determine if the word is used
        #frequently enough to be determined a gamer word
        elif word not in normal_dictionary and gamer_dictionary[word] > .00005:
            gamer_words.append(word)
    return gamer_words



def parse_words(normal_dictionary, gamer_dictionary, threshold):
    """
    Parse through a dictionary of words and their frequencies in "gamer" and
    "normal" subreddits to find meaningfully different language patterns
    between the two word sets

    Returns:
        gamer_dictionary: a dictionary with strings as keys and floats as the
            values representing what percentage of the time that string gets 
            used in the dataset
        normal_dictionary: a dictionary with strings as keys and floats as the
            values representing what percentage of the time that string gets 
            used in the dataset
        gamer_words:
            a list of strings representing words determined to be meaningfully 
            distinct to the gamer vocabulary
    
    """
    #print(len(gamer_dictionary))
    gamer_dictionary = remove_too_uncommon(gamer_dictionary,threshold)
    normal_dictionary = remove_too_uncommon(normal_dictionary,threshold)
    #print(len(gamer_dictionary))
    #curate the dictionary sets
    normal_dictionary, gamer_dictionary, ignore_list = remove_most_common(normal_dictionary\
        , gamer_dictionary)
    #print(len(gamer_dictionary))

    #determine gamer words
    gamer_words = determine_gamer_words(normal_dictionary,gamer_dictionary)

    return normal_dictionary,gamer_dictionary,gamer_words, ignore_list



def determine_language_similarity(word_dictionary, user_dictionary):

    """
    Determine how similar a user's vocabulary is to a certain curated language
    set

    Args:
        word_dictionary: a dictionary with strings as keys and floats as values
        representing how frequently a word is used in a set of words
        user_dictionary: a dictionary with strings as keys and floats as values
        representing how frequently a word is used in a set of words
    Returns:
        a float representing how close a user's total language usage is to a
        given set of data with lower numbers being closer
    """
    difference_list = []
    #we specifically iterate through the user's list of used words because this
    #list will be smaller by necessity than the words used by the entire
    #dataset of users in a subreddit. It would therefore be unfair to judge
    #closeness of a user's language used by the amount of words that they do
    #not use that appear in a given dataset.
    for word in user_dictionary:
        if word in word_dictionary:
            difference_list.append((user_dictionary[word] - word_dictionary\
                [word])**2)
        else:
            difference_list.append(user_dictionary[word]**2)
    
    return math.sqrt(sum(difference_list))

