"""
Test library functions to find and identify protein-coding genes in DNA.
"""
from collections import Counter
import pytest

from gamer_words import (
    find_most_frequent,
    instances_to_decimal,
    remove_most_common,
    remove_too_uncommon,
    determine_gamer_words,
    determine_language_similarity,
    is_gamer,
)


# Define sets of test cases.
find_most_frequent_cases = [
    # Check that the simplest dictionary case returns correctly
    ({"cheese":1}, 1, {"cheese":1}),
    # Check that asking for no items returns an empty dictionary
    ({"pedestrian":1}, 0, {}),
    # Check that a dictionary of 2 items returns items in the correct order
    ({"cheese":1,"pedestrian":3,}, 2, {"pedestrian":3,"cheese":1}),
    # Check that the function can exclude cases if less words are asked for than
    # are in the dictionary
    ({"cheese":1,"cheezits":4,"cheetos":7}, 2, {"cheetos":7,"cheezits":4})
    

    
]

instances_to_decimal_cases = [
    # Check that the simplest case of the function works
    ({"cheese":1},{"cheese":1},1),
    # Check that single word inputs always result in one
    ({"cheese":10101},{"cheese":1},10101),
    # Check that a simple dictionary with multiple words with positive integer
    # values functions
    ({"cheese":1,"malt":2},{"cheese":1/3,"malt":2/3},3),
    # Check that if the sum of the values of the dictionary is 0, then the
    # function returns an empty dictionary
    ({"cheese":0,"malt":0},{},0)


]

remove_most_common_cases = [
    # Check that a blank normal dictionary does not remove any words from the
    # gamer dictionary
    ({},{"game":.1,"gaming":.6,"poggers":.3},0,1 \
        ,{},{"game":.1,"gaming":.6,"poggers":.3},[]),
    
    # Check a simple case where a word gets removed
    ({"game":.13},{"game":.1,"gaming":.7,"poggers":.5},1,1,\
        {},{"gaming":.7/1.2,"poggers":.5/1.2},["game"]),

    # Check more complex case where some words get removed, some words are 
    # different in each dictionary and the total number of words in each 
    # dictionary is both not one and not the same
    ({"game":.13,"poggers":1,"gaming":.65,"soul":1},{"game":.1,"gaming":.7,"salmon":.4,"poggers":.6},3,4,\
        {"poggers":1/(1 + 1),"soul":1/(1 + 1)},{"salmon":.4/1,"poggers":.6/1},["game","gaming"]),




]

remove_too_uncommon_cases = [
    # Test a simple case with clearly removable entries and a threshold equal to
    # one of the values of a key
   ({"gamers":1,"pasta":24,"notgamer":4,"gamingaminggaming":2},4,\
       {"pasta":24,"notgamer":4}),
    # Test that keys of the form "wordcword" get removed
    ({"mochacmocha":101010101,"gamers":6,"aditicaditi":85,"lukecaditi":16,\
        "pastacpasta":2},3,{"gamers":6,"lukecaditi":16}),
    # Check that overly long entries are removed
    ({"asfdljkasfdladsfjksfdakhasfdlfsda":110},2,{}),
    # Check an empty dictionary
    ({},0,{})

    

]

determine_gamer_words_cases = [
    # Check a simple case with a gamer word that is used drastically more in the
    # Gamer dictionary than the normal dictionary
    ({"gaming":.01,"pogggg":.01},{"gaming":.1,"pogggg":.05},["gaming"]),
    # Check that a gamer word that isn't in the normal dictionary makes the list
    ({"blame":.152},{"blame":.153,"sled":.000078,"sleigh":.00008},["sleigh"]),
    # Check that a word that shows up a substantially different amount in the
    # normal and gamer dictionaries but is used less in the gamer dictionary is
    # not considered a gamer word
    ({"fantasy":1},{"fantasy":.000000000000001},[])
]

# The parse_words function is composed entirely of the previous functions and
# thus does not need unit tests, or rather the unit tests for this function 
# would fundamentally test the same things as the previous unit tests

determine_language_similarity_cases = [
    # Check that an empty language dictionary outputs the sum of the squares
    # of the user dictionary
    ({},{"gaming":3,"gamers":4},5),
    # Theck that if the user and language dictionaries are the same that
    # the result is 0
    ({"gaming":3,"gamers":4},{"gaming":3,"gamers":4},0),
    # Check a case with words in both dictionaries but with with unequal values
    ({"gaming":2,"gamers":4},{"gaming":5,"gamers":8},5),
]

# The parse_words function does not have any unit tests written for it as it
# is exclusively a combination of other functions that all have unit tests, and
# as a result, we are sure that the inner workings of the function work as
# intended.

# The analyze_users_language function does not have any unit tests written for it
# because it requires a folder full of csv's to run, which would be ridiculous
# to create for unit tests. Also, nearly every component of this function is
# combinations of other functions that have unit tests, so we are confident that
# the inner workings of the function function as intended. The fact that we
# recieve usable and vizualizable data from this function has allowed us to
# be confident that it works.

# stats_and_z_info is required to run through a folder full of CSV's to test;
# since that would be too difficult to simulate, testing on the components
# alone should be more than enough to ensure that the function works.

is_gamer_cases = [
    # Check that a negative and a positive z-value return True
    
  

]


# Define standard testing functions to check functions' outputs given certain
# inputs defined above.
@pytest.mark.parametrize("freq_input_dict,freq_input_int,output_dict", find_most_frequent_cases)
def test_find_most_frequent(freq_input_dict, freq_input_int, output_dict):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    assert find_most_frequent(freq_input_dict, freq_input_int) == output_dict


@pytest.mark.parametrize("input_dictionary,output_dictionary,total_words",
                         instances_to_decimal_cases)
def test_instances_to_decimal(input_dictionary, output_dictionary,total_words):
    """
    Test that the instance_to_decimal function properly converts from integers
    to floats.

    Args:
        input_dictionary: A dictionary with strings as keys and positive 
            integers as values.
        output_dictionary: A dictionary with strings as keys and floats as
            values.
        total_words: An integer that is the sum of the values in the input
            dictionary representing the total number of words used is a language
            set.

    """
    assert instances_to_decimal(input_dictionary) == (output_dictionary,total_words)


@pytest.mark.parametrize("normal_dictionary,gamer_dictionary,normal_total_words,gamer_total_words,normal_dict_out,\
gamer_dict_out,ignore_list_out", remove_most_common_cases)
def test_remove_most_common(normal_dictionary, gamer_dictionary,normal_total_words,gamer_total_words,normal_dict_out,\
    gamer_dict_out,ignore_list_out):
    """
    Test that the remove_most_common function removes the words that it should
    be removing.

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
        normal_dict_out = A dictionary with strings as keys representing
            words and floats as values representing what ratio of the time a 
            word gets used in the normal dataset.
        gamer_dict_out = A dictionary with strings as keys representing words 
            and floats as values representing what ratio of the time a word gets
            used in the gamer dataset.
        ignore_list_out = A list of strings containing words which were omitted
            from both dictionaries.

    """
    assert remove_most_common(normal_dictionary, gamer_dictionary,normal_total_words,gamer_total_words) == \
        (normal_dict_out,gamer_dict_out,ignore_list_out)

@pytest.mark.parametrize("dictionary,threshold,dictionary_out", remove_too_uncommon_cases)
def test_remove_too_uncommon(dictionary,threshold,dictionary_out):
    """

    Test that remove_too_uncommon removes typos, overly long strings, and words
    that do not show up frequently as it should be.

    Args:
        dictionary: A dictionary with strings as keys representing words 
            and integers as values representing how many times that word
            is used in a dataset.
        threshold: An integer determining the minimum number of usages for a 
            word to be considered in the dictionary.
        dictionary_out: A dictionary with strings as keys representing 
            words and integers as values representing how many times that word
            is used in a dataset.
    """
    assert remove_too_uncommon(dictionary,threshold) == dictionary_out


@pytest.mark.parametrize("normal_dictionary,gamer_dictionary,word_list", determine_gamer_words_cases)
def test_determine_gamer_words(normal_dictionary, gamer_dictionary,word_list):
    """
    Test that the determine_gamer_words() function properly finds language
    very commonly used by gamers.

    Args:
        normal_dictionary: A dictionary with strings as keys and floats as the
            values representing what ratio of the time that string gets 
            used in the dataset.
        gamer_dictionary: A dictionary with strings as keys and floats as the
            values representing what ratio of the time that string gets 
            used in the dataset.
        word_list: A list of strings representing words specific to the
            gamer vocabulary.
    
    """
    assert determine_gamer_words(normal_dictionary,gamer_dictionary) == word_list


@pytest.mark.parametrize("language_dict,user_dict,closeness_value", determine_language_similarity_cases)
def test_determine_language_similarity(language_dict, user_dict,closeness_value):
    """
    Test that the determine_language_similarity() function properly determines
    closeness values between user and community language datasets.

    Args:
        language_dict: A dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in a language dataset.
        user_dict: A dictionary with strings as keys and floats
            as the values representing what ratio of the time that string gets 
            used in a user's personal language dataset.
        closeness_value: A float representing how close a user's total language 
            usage is to a given set of data with lower numbers being closer.
    """
    assert determine_language_similarity(language_dict,user_dict) == closeness_value


@pytest.mark.parametrize("strand,orf", is_gamer_cases)
def test_is_gamer(gamer_z, normal_z, gamer_status):
    """
    Determine whether or not the is_gamer() function properly determines
    whether a user is a gamer or not based on their gamer and normal 
    z-scores.

    """
    assert is_gamer(gamer_z, normal_z) == gamer_status

