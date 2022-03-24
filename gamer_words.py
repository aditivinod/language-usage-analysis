#take a dictionary of words and their relative frequency and parse through the
#data to find specific "gamer words"

example_dict = {"gamer":1, "gamers":2, "gaming":3, "the": 7, "potassium": 9, \
"potassiums" : 9
}
#import nltk and WordNetLemmatizer for detecting plural words
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()

def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma

def depluralize(frequency_dictionary):
    """
    Take a dictionary whose keys are a list of words and values are the number
    of times that word showed up in a subreddit and remove duplicate words that
    are plurals by combining the keys into one key and adding the values.

    Args:
        frequency_dictionary: a dictionary with words as keys and integers as
        values
    """
    not_plural_dict = {}
    ignore_list = []
    for word in frequency_dictionary:
        
        plural, lemma = isplural(word)

        #if the word is not plural, skip the loop
        if plural is False:
            ignore_list.append(word)
            continue

        if lemma in frequency_dictionary:
            not_plural_dict[lemma] = frequency_dictionary[lemma] \
                + frequency_dictionary[word]
            ignore_list.append(word)
    
    for word in ignore_list not in not_plural_dict:
        not_plural_dict[word] = frequency_dictionary[word]

        #for indexed_word in frequency_dictionary:
            #check if the indexed word is a plural version of the original word
           
           
        """ if word + "s" == indexed_word or word + "es" == indexed_word or \
            word + "en" == indexed_word or word + "'s" == indexed_word:

            not_plural_dict[word] = frequency_dictionary[indexed_word] \
                + frequency_dictionary[word]

            ignore_list.append(indexed_word)
            break"""
        
    
    return not_plural_dict
print(depluralize(example_dict))

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
        
    """
    #convert values from the number of times a word is used to the frequency
    #of times the word is used total for both the normal and gamer dictionaries
    normal_total_words = sum(normal_dictionary.values())
    for word in normal_dictionary:
        normal_dictionary[word] = normal_dictionary[word]/normal_total_words
    
    gamer_total_words = sum(gamer_dictionary.values())
    for word in normal_dictionary:
        gamer_dictionary[word] = gamer_dictionary[word]/gamer_total_words
    
    ignore_list = []
    for word in normal_dictionary:

        if word in gamer_dictionary and normal_dictionary[word]*1.15 > \
            gamer_dictionary[word] > normal_dictionary[word]*.85:

            ignore_list.append(word)
            gamer_dictionary.pop(word)
        
    for word in ignore_list:
        normal_dictionary.pop(word)
    
    return normal_dictionary,gamer_dictionary

def remove_too_uncommon(word_dictionary, threshold):
    """
    remove words from the dictionary that show up less than a specified
    number of times

    Args:
        word_dictionary: a dictionary with words as keys and integers as values
        threshold: an integer determining the minimum number of usages for a 
            word to be considered in the dictionary
    
    """

    delete_word = [key for key in word_dictionary if word_dictionary[key] < \
        threshold]
    
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
            gamer_dictionary[word]/50:
            gamer_words.append(word)
        #if the word is not present in the normal dictionary, then use a simple
        #percentage of uses comparison to determine if the word is used
        #frequently enough to be determined a gamer word
        elif word not in normal_dictionary and gamer_dictionary[word] > .00005:
            gamer_words.append(word)
    return gamer_words



def parse_words(normal_dictionary, gamer_dictionary):
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

    gamer_dictionary = depluralize(gamer_dictionary)
    normal_dictionary = depluralize(normal_dictionary)

    gamer_dictionary = remove_too_uncommon(gamer_dictionary,3)
    normal_dictionary = remove_too_uncommon(normal_dictionary,3)
    #curate the dictionary sets
    normal_dictionary, gamer_dictionary = remove_most_common(normal_dictionary\
        , gamer_dictionary)
    
    #determine gamer words
    gamer_words = determine_gamer_words(normal_dictionary,gamer_dictionary)

    return normal_dictionary,gamer_dictionary,gamer_words



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
                [word])^2)
        else:
            difference_list.append(user_dictionary[word]^2)
    
    return sum(difference_list)

