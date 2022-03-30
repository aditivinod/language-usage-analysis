#take a dictionary of words and their relative frequency and parse through the
#data to find specific "gamer words"

example_dict = {"gamer":1, "gamers":2, "gaming":3, "the": 7, "potassium": 9, \
"potassiums" : 9
}

from operator import itemgetter
import math
import os
from scrape_data import csv_to_dict

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
    return_dict = {}
    total_words = sum(dictionary.values())
    for word in dictionary:
        return_dict[word] = dictionary[word]/total_words
    return return_dict

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

        if word in gamer_dictionary and normal_dictionary[word]*1.25 > \
            gamer_dictionary[word] > normal_dictionary[word]*.75:

            ignore_list.append(word)
            
        
    normal_return_dict = {word:value for (word,value) in normal_dictionary.items() if word not in ignore_list }
    gamer_return_dict = {word:value for (word,value) in gamer_dictionary.items() if word not in ignore_list }

    return normal_return_dict,gamer_return_dict, ignore_list

def remove_too_uncommon(word_dictionary, threshold =20):
    """
    remove words from the dictionary that show up less than a specified
    number of times. Also remove entries that are strings longer than length 20

    Args:
        word_dictionary: a dictionary with words as keys and integers as values
        threshold: an integer determining the minimum number of usages for a 
            word to be considered in the dictionary
    
    """

    delete_word = [key for key in dict(word_dictionary).keys() if int(word_dictionary[key]) \
        < threshold or len(key) > 20]
    
    #remove typo words that repeat themselves of the form "wordcword"
    for key in dict(word_dictionary).keys():
        if key not in delete_word and "c" in key and (len(key) - 1) % 2 == 0:
            half_word = key[0:int((len(key)-1)/2)]
            if half_word in key[int(((len(key)-1)/2)+1):len(key)]:
                delete_word.append(key)
    
    for key in delete_word: word_dictionary.pop(key)
    word_return_dictionary = {word:value for (word,value) in word_dictionary.items() if word not in delete_word }


    return word_return_dictionary

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
        if (word in normal_dictionary )and (normal_dictionary[word] <\
            gamer_dictionary[word]/8):
            gamer_words.append(word)
        #if the word is not present in the normal dictionary, then use a simple
        #percentage of uses comparison to determine if the word is used
        #frequently enough to be determined a gamer word
        elif (word not in normal_dictionary) and (gamer_dictionary[word] > .000079):
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
    working_gamer_dictionary = remove_too_uncommon(gamer_dictionary,threshold)
    working_normal_dictionary = remove_too_uncommon(normal_dictionary,threshold)
    #print(len(gamer_dictionary))
    #curate the dictionary sets
    working_normal_dictionary = instances_to_decimal(working_normal_dictionary)
    working_gamer_dictionary = instances_to_decimal(working_gamer_dictionary)

    working_normal_dictionary, working_gamer_dictionary, ignore_list = remove_most_common(working_normal_dictionary\
        , working_gamer_dictionary)
    #print(len(gamer_dictionary))

    #determine gamer words
    gamer_words = determine_gamer_words(working_normal_dictionary,working_gamer_dictionary)

    return working_normal_dictionary, working_gamer_dictionary, gamer_words, \
        ignore_list



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

def analyze_users_language(normal_dictionary, gamer_dictionary, gamer_words, ignore_list, folder_path):
    """
    Analyze a user's language similarity to a dictionary
    
    Returns:
        dictionary -> key is filepath,values is list [normal closeness val, gamer closeness val, ratio of gamer words used to all words]
    """
    file_list = os.listdir(folder_path)

    file_list = [folder_path +"/" + user for user in file_list]

    #print(file_list)

    user_value_dict = {}
    swap_list = []
    for user in file_list:

        swap_list = []
        user_dictionary = csv_to_dict(user)
        
        #remove non useful user data
        user_dictionary = remove_too_uncommon(user_dictionary,1)
        user_dictionary = {word:value for (word,value) in user_dictionary.items() if word not in ignore_list}
        user_dictionary = instances_to_decimal(user_dictionary)

        #print(user_dictionary)
        #print(type(user_dictionary))
        swap_list.append(determine_language_similarity(normal_dictionary,user_dictionary))
        swap_list.append(determine_language_similarity(gamer_dictionary,user_dictionary))
        
        #compute what ratio of words that a user uses are gamer words
        ratio_gamer_words_used = 0
        for word in gamer_words:
            if word in user_dictionary.keys():
                ratio_gamer_words_used += user_dictionary[word]
        ratio_gamer_words_used = ratio_gamer_words_used/sum(user_dictionary.values())
        swap_list.append(ratio_gamer_words_used)

        user_value_dict[user] = swap_list

    return user_value_dict

def stats_lists(stats_dict, folder_path):
    file_list = get_file_list(folder_path)

    normal_closeness = []
    gamer_closeness = []
    gamer_all_ratio = []

    for user in file_list:
        normal_closeness.append(stats_dict[user][0])
        gamer_closeness.append(stats_dict[user][1])
        gamer_all_ratio.append(stats_dict[user][2])
    
    return [normal_closeness, gamer_closeness, gamer_all_ratio]

def is_gamer():
    

def get_file_list(folder_path):
    file_list = os.listdir(folder_path)
    file_list = [folder_path +"/" + user for user in file_list]
    return file_list

def find_most_frequent_gamer_words(user_dict, gamer_words, num_items):
    user_gamer_words = {}
    for word in user_dict:
        if word in gamer_words:
            user_gamer_words[word] = user_dict[word]
    
    return find_most_frequent(user_gamer_words, num_items)
    


