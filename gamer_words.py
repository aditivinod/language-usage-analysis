# Take a dictionary of words and their relative frequency and parse through the
#data to find specific "gamer words"

from operator import itemgetter
import math
import os
from types import WrapperDescriptorType
import numpy as np

from sympy import true
from scrape_data import csv_to_dict

def find_most_frequent(word_dictionary, number_items):
    """
    Find a specified number of keys from a dictionary that have the highest
    integer values.

    Args:
        word_dictionary: A dictionary with strings as keys and positive
            integers as values.
        number_items: An integer determining how many value ordered items to
            output.
    Returns:
        most_frequent_dictionary: A value ordered dictionary with strings as
            keys and integers as values.
    """
    most_frequent_dictionary = dict(sorted(word_dictionary.items(), key = \
        itemgetter(1), reverse = True)[:number_items])
    
    return most_frequent_dictionary



def instances_to_decimal(dictionary):
    """
    Convert the values of a dictionary from an integer to a decimal ratio
    of what frequency of the time that word is used in the total dataset.

    Args:
        dictionary: A dictionary with strings as keys and positive integers
            as values.
    Returns:
        return_dict: A dictionary with strings as keys and floats as values.
        total_words: An integer that is the sum of the values in the input
            dictionary representing the total number of words used is a language
            set.
    """
    return_dict = {}
    total_words = sum(dictionary.values())
    # Avoids 0 division error
    if total_words <= 0:
        return return_dict, total_words
    for word in dictionary:
        return_dict[word] = dictionary[word]/total_words
    return return_dict, total_words

def remove_most_common(normal_dictionary, gamer_dictionary,normal_total_words, \
    gamer_total_words):
    """
    Remove words between dictionaries that show up similarly frequently between
    the "normal" dataset and the "gamer" dataset.

    Args:
        normal_dictionary = A dictionary with strings as keys representing words 
            and floats as values representing what ratio of the time a word gets
            used in the normal dataset
        gamer_dictionary = A dictionary with strings as keys representing words 
            and floats as values representing what ratio of the time a word gets
            used in the gamer dataset
        normal_total_words: An integer representing the total instances of
            word uses in the normal dataset
        gamer_total_words: An integer representing the total instances of
            word uses in the gamer dataset
    Returns:
        normal_return_dict = A dictionary with strings as keys representing
            words and floats as values representing what ratio of the time a 
            word gets used in the normal dataset.
        gamer_return_dict = A dictionary with strings as keys representing words 
            and floats as values representing what ratio of the time a word gets
            used in the gamer dataset.
        ignore_list = A list of strings containing words which were omitted
            from both dictionaries.
        
    """
    ignore_list = []
    # Create list of words to ignore
    for word in normal_dictionary:
        if word in gamer_dictionary and normal_dictionary[word]*1.25 > \
            gamer_dictionary[word] > normal_dictionary[word]*.75:

            ignore_list.append(word)
    
    # What to do if nothing is in the normal dictionary  
    if normal_total_words == 0:
        normal_return_dict = {}
        gamer_return_dict = {word:value for (word,value) in \
            gamer_dictionary.items()}
        return normal_return_dict, gamer_return_dict, ignore_list
    # What to do if nothing is in the gamer dictionary
    elif gamer_total_words == 0:
        normal_return_dict = {word:value for (word,value) in \
            normal_dictionary.items()}
        gamer_return_dict = {word:value*gamer_total_words for (word,value) in \
            gamer_dictionary.items()}
        return normal_return_dict, gamer_return_dict, ignore_list

    # Turn the decimal dictionaries into frequency dictionaries
    normal_return_dict = {word:value*normal_total_words for (word,value) in\
         normal_dictionary.items() if word not in ignore_list}
    gamer_return_dict = {word:value*gamer_total_words for (word,value) in \
        gamer_dictionary.items() if word not in ignore_list}
    
    # Find the sum of all values in both frequency dictionaries
    new_gamer_total_words = sum(gamer_return_dict.values())
    new_normal_total_words = sum(normal_return_dict.values())
    # Divide the frequency dictionaries by the total values in each dictionary
    normal_return_dict = {word:value/new_normal_total_words for (word,value)\
         in normal_return_dict.items()}
    gamer_return_dict = {word:value/new_gamer_total_words for (word,value) \
        in gamer_return_dict.items() }

    return normal_return_dict,gamer_return_dict, ignore_list

def remove_too_uncommon(word_dictionary, threshold =20):
    """
    Remove words from a dictionary that show up less than a specified
    number of times. Also remove entries that are strings longer than length 20
    or words that fall into a specific type of typo.

    Args:
        word_dictionary: A dictionary with strings as keys representing words 
            and integers as values representing how many times that word
            is used in a dataset.
        threshold: An integer determining the minimum number of usages for a 
            word to be considered in the dictionary.
    Returns:
        word_return_dictionary: A dictionary with strings as keys representing 
            words and integers as values representing how many times that word
            is used in a dataset.
    """

    delete_word = [key for key in dict(word_dictionary).keys() if \
        int(word_dictionary[key]) < threshold or len(key) > 20]
    
    # Remove typo words that repeat themselves of the form "wordcword"
    for key in dict(word_dictionary).keys():
        if key not in delete_word and "c" in key and (len(key) - 1) % 2 == 0:
            half_word = key[0:int((len(key)-1)/2)]
            if half_word in key[int(((len(key)-1)/2)+1):len(key)]:
                delete_word.append(key)
    
    # For key in delete_word: word_dictionary.pop(key)
    word_return_dictionary = {word:value for (word,value) in \
        word_dictionary.items() if word not in delete_word }


    return word_return_dictionary

def determine_gamer_words(normal_dictionary,gamer_dictionary):

    """
    Determine words specific to a language set by comparing and finding words
    that are used significantly more frequently by a community than the general
    populace.

    Args:
        normal_dictionary: A dictionary with strings as keys and floats as the
            values representing what ratio of the time that string gets 
            used in the dataset.
        gamer_dictionary: A dictionary with strings as keys and floats as the
            values representing what ratio of the time that string gets 
            used in the dataset.
    Returns:
        gamer_words: A list of strings representing words specific to the
            gamer vocabulary.
    """
    gamer_words = []

    for word in gamer_dictionary:
        # Determine a word to be a gamer word if it is used 50 times more
        # frequently in gamer subreddits than normal subreddits
        if (word in normal_dictionary) and (normal_dictionary[word] <\
            gamer_dictionary[word]/8):
            gamer_words.append(word)
        # If the word is not present in the normal dictionary, then use a simple
        # percentage of uses comparison to determine if the word is used
        # frequently enough to be determined a gamer word
        elif (word not in normal_dictionary) and (gamer_dictionary[word] >\
             .000079):
            gamer_words.append(word)
    return gamer_words

def parse_words(normal_dictionary, gamer_dictionary, threshold):
    """
    Parse through a dictionary of words and their frequencies in "gamer" and
    "normal" subreddits to find meaningfully different language patterns
    between the two word sets.

    Args:
        normal_dictionary = A dictionary with strings as keys representing words
            and integers as values representing the number of times a word
            gets used in the normal dataset
        gamer_dictionary = A dictionary with strings as keys representing words 
            and integers as values representing the number of times a word
            gets used in the gamer dataset
        threshold: An integer determining the minimum number of usages for a 
            word to be considered in the dictionary for use in the
            remove_too_uncommon function()
    Returns:
        working_normal_dictionary: a dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in the normal dataset.
        working_gamer_dictionary: a dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in the gamer dataset.
        gamer_words: a list of strings representing words determined to be 
            meaningfully distinct to the gamer vocabulary.
        ignore_list = a list of strings representing the words that were
            removed from the original word dictionaries in this function
    """
    # Curate dictionary sets for word usages
    working_gamer_dictionary = remove_too_uncommon(gamer_dictionary,threshold)
    working_normal_dictionary = remove_too_uncommon(normal_dictionary,threshold)
    # Change from a word frequency list to a ratio of the amount of times that
    # word is used
    working_normal_dictionary, normal_total_words = \
        instances_to_decimal(working_normal_dictionary)
    working_gamer_dictionary, gamer_total_words = \
        instances_to_decimal(working_gamer_dictionary)
    # Curate dictionaries by comparing them to each other
    working_normal_dictionary, working_gamer_dictionary, ignore_list = \
        remove_most_common(working_normal_dictionary\
        , working_gamer_dictionary, normal_total_words, gamer_total_words)

    # Determine gamer words
    gamer_words = determine_gamer_words(working_normal_dictionary,\
        working_gamer_dictionary)

    return working_normal_dictionary, working_gamer_dictionary, gamer_words, \
        ignore_list



def determine_language_similarity(word_dictionary, user_dictionary):
    """
    Determine how similar a user's vocabulary is to a certain curated language
    set with lower numbers determining closer similarities in language. 
    
    If every word that a user types is considered a dimension in vector
    space, then one can construct a vector for a user's dataset and a vector
    for the community language dataset by setting the magnitude of each vector
    component as the ratio of times a certain word is used total in the user and
    community language dataset respectively. One can then quantify how close
    these two language datasets are to each other by subtracting these two
    vectors and finding the magnitude of the resultant vector.

    Args:
        word_dictionary: A dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in a language dataset.
        user_dictionary: A dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in a user's personal language dataset.
    Returns: 
        A float representing how close a user's total language usage is to  a given
            set of data with lower numbers being closer.
    """
    difference_list = []
    # We specifically iterate through the user's list of used words because this
    # list will be smaller by necessity than the words used by the entire
    # dataset of users in a subreddit. It would therefore be unfair to judge
    # closeness of a user's language used by the amount of words that they do
    # not use that appear in a given dataset.
    for word in user_dictionary:
        if word in word_dictionary:
            difference_list.append((user_dictionary[word] - word_dictionary\
                [word])**2)
        else:
            difference_list.append(user_dictionary[word]**2)
    
    return math.sqrt(sum(difference_list))

def analyze_users_language(normal_dictionary, gamer_dictionary, gamer_words,\
     ignore_list, folder_path):
    """
    Analyze a set of several user's language usage data, stored in
    a folder as csv's, similarity to a normal and gamer language set and output
    the result.
    
    Args:
        normal_dictionary: A curated dictionary with strings as keys and floats
            as the values representing the number of the time that string gets 
            used in the normal dataset.
        gamer_dictionary: A curated dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in the gamer dataset.
        gamer_words: A list of strings representing words used much more
            commonly by gamers than non gamers.
        ignore_list: A list of strings representing words to remove from a
            user's language set
        folder_path: A string representing the relative path of the folder that
            all of the user data csv's are in.
    Returns:
        user_value_dictionary: A dictionary with a string representing the
            relative file path of a user's language usage data as a key and a
            list of integers as the value. The list value is of the form:
            [normal_closeness, gamer_closeness, ratio_gamer_words_used]
        normal_closeness: An integer representing how close a user's language
            usage is to the normal dataset.
        gamer_closeness: An integer representing how close a user's language
            usage is to the gamer dataset.
        ratio_gamer_wordS_used: An integer representing the ratio of gamer words
            used by a user out of all of the words they use.
    """
    # Create a list of user csv file paths
    file_list = get_file_list(folder_path)

    user_value_dict = {}
    swap_list = []
    # Iterate through users
    for user in file_list:

        swap_list = []
        # Create a dictionary from the user csv
        user_dictionary = csv_to_dict(user)
        
        # Remove non useful user data
        user_dictionary = remove_too_uncommon(user_dictionary,1)
        user_dictionary = {word:value for (word,value) in \
            user_dictionary.items() if word not in ignore_list}

        # Make the values of the user dictionary a ratio
        user_dictionary, _ = instances_to_decimal(user_dictionary)

        # Append to the user's output list their closeness values for the
        # Normal language set and gamer language set in that order
        swap_list.append(determine_language_similarity(normal_dictionary,user_dictionary))
        swap_list.append(determine_language_similarity(gamer_dictionary,user_dictionary))
        
        # Compute what ratio of words that a user uses are gamer words
        ratio_gamer_words_used = 0
        for word in gamer_words:
            if word in user_dictionary.keys():
                ratio_gamer_words_used += user_dictionary[word]
        ratio_gamer_words_used = ratio_gamer_words_used/sum(user_dictionary.values())
        # Append to a user's ouput list the ratio of gamer words they use
        swap_list.append(ratio_gamer_words_used)

        user_value_dict[user] = swap_list

    return user_value_dict

def stats_and_z_info(stats_dict, folder_path):
    """
    Given a dictionary containing users and their respective analysis
    statistics, generates the overall statsistics lists, and the z-score values
    for each user.

    Args:
        stats_dict: A dictionary representing all of the testing users'
            statistics. The keys are strings representing the user CSV file
            paths and the values are a list containing the two closeness stats
            and the gamer:all words ratio.
        folder_path: A string representing the path to the folder containing
            all of the test user CSVs.
    Returns: 
        stats: A list of three lists containing floats; each float list
            contains the data for a singular statistic from the user analysis
            for all of the users.
        z_dict: A dictionary representing all of the testing users' z-scores
            for closeness to the gamer and normal words. The keys are strings
            representing the user CSV file paths and the values are lists 
            containing one index per z-score.
        z_list: A list containing two lists of floats, one per z-value, for all
            of the testing users.
    """
    # Stats dict is output of analyze users_language
    file_list = get_file_list(folder_path)

    normal_closeness = []
    gamer_closeness = []
    gamer_all_ratio = []

    # Calculate stats lists
    for user in file_list:
        normal_closeness.append(stats_dict[user][0])
        gamer_closeness.append(stats_dict[user][1])
        gamer_all_ratio.append(stats_dict[user][2])    
    stats = [normal_closeness, gamer_closeness, gamer_all_ratio]

    # Calculate means & standard deviations
    mean_normal = sum(stats[0])/len(stats[0])
    std_normal = np.std(stats[0])

    mean_gamer = sum(stats[1])/len(stats[1])
    std_gamer = np.std(stats[1])

    # Form z dict
    z_dict = {}
    norm_list = []
    gamer_list = []
    for user in file_list:
        z_normal = (stats_dict[user][0]-mean_normal)/std_normal
        z_gamer = (stats_dict[user][1]-mean_gamer)/std_gamer
        z_dict[user] = [z_normal, z_gamer]
        norm_list.append(z_normal)
        gamer_list.append(z_gamer)
    z_lists = [norm_list, gamer_list]
   

    return stats, z_dict, z_lists

"""
Determines whether an individual user is considered a gamer or not.

Args:
    gamer_z: The individual user's z-score for closeness to the gamer words.
    normal_z: The individual user's z-score for closeness to the normal words.
"""
def is_gamer(gamer_z, normal_z):
    if gamer_z-normal_z < 0:
        return True
    return False

"""
Gets a list of all the files given a folder path.

Args:
    Folder path: A string representing a path to the folder containing the test
        users' CSVs.
Returns:
    A list of strings representing the paths to each of the individual users'
        CSV files.
"""
def get_file_list(folder_path):
    file_list = os.listdir(folder_path)
    file_list = [folder_path +"/" + user for user in file_list]
    return file_list

"""
Given a users' frequency dictionary and a number, determines the most frequent
gamer words up to that number.

Args: 
    user_dict: A dictionary representing an individual user's word frequencies.
        The keys are strings reprenting the words that the user has said and
        the values are integers representing how many times the corresponding
        key has been sent as a message by the user.
    gamer_words: A list of strings representing the gamer words.
    num_items: The number of gamer_words to output.
Returns:
    A dictionary representing the most frequent gamer words present in the
    users' messages. The keys are strings representing the gamer words and
    the values are numbers representing their corresponding frequencies.
"""
def find_most_frequent_gamer_words(user_dict, gamer_words, num_items):
    user_gamer_words = {}
    for word in user_dict:
        if word in gamer_words:
            user_gamer_words[word] = user_dict[word]
    
    return find_most_frequent(user_gamer_words, num_items)

def determine_gamer_words_frequency(normal_dictionary, gamer_dictionary):
    """
    Creates a frequency dictionary for the gamer words list.

    Args:
        normal_dictionary: A dictionary representing the normal words prior to
            removal of overly common terms. The keys are strings representing
            the words and the values are integers representing their
            corresponding frequencies.
        gamer_dictionary: A dictionary representing the gamer words prior to 
            removal of overly common terms. The keys are strings representing
            the words and the values are integers representing their
            corresponding frequencies.
    Returns:
        A dictionary representing the gamer words. The keys are strings
        representing the words and the values are integers representing 
        their corresponding frequencies.
    """
    gamer_words = {}
    
    for word in gamer_dictionary:
        # Determine a word to be a gamer word if it is used 50 times more
        # frequently in gamer subreddits than normal subreddits
        if word in normal_dictionary and normal_dictionary[word] <\
            gamer_dictionary[word]/8:
            gamer_words[word] = gamer_dictionary[word]
        # Ff the word is not present in the normal dictionary, then use a simple
        # percentage of uses comparison to determine if the word is used
        # frequently enough to be determined a gamer word
        elif (word not in normal_dictionary) and (gamer_dictionary[word] > .000079):
            gamer_words[word] = gamer_dictionary[word]
    return gamer_words
    
    
def generate_user_id_dict(z_dict, user_stats_dict, gamer_words, folder_path):
    """
    Generates the info necessary to create the individual user ID cards.

    Args:
        z_dict: A dictionary representing the z-scores for each individual user.
            The keys are strings representing the path to the users' data and
            the values are a list containing two z-scores.
        user_stats_dict: A dictionary representing the stats for each
            individual user. The keys are strings representing the path to the
            users' data and the values are a list containing the three primary
            stats calculated for each user.
        gamer_words: A list of strings represenging the gamer words.
        folder_path: A string representing the path to the folder containing
            all the individual users' data.
    Returns:
        user_id_dict: A dictionary representing the information that goes on
            each individual users' ID card. The keys are strings representing
            the path to the users' data and the values are a list containing 
            the information necessary for the ID card.
    """
    user_id_dict = {}

    file_list = get_file_list(folder_path)

    for user in file_list:
        username = str(user)[len(str(folder_path))+1:-4]
        gamer_z = z_dict[user][1]
        normal_z = z_dict[user][0]
        gamer_status = is_gamer(gamer_z, normal_z)
        gamer_all_freq = user_stats_dict[user][2]
        top = list(find_most_frequent_gamer_words(csv_to_dict(user), gamer_words, 5).keys())

        id_info = [username, gamer_status, gamer_z, normal_z, gamer_all_freq, top]
        user_id_dict[user] = id_info
    
    return user_id_dict