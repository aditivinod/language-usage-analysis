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
    #check that asking for no items returns an empty dictionary
    ({"pedestrian":1}, 0, {}),
    #check that a dictionary of 2 items returns items in the correct order
    ({"cheese":1,"pedestrian":3,}, 2, {"pedestrian":3,"cheese":1}),
    #check that the function can exclude cases if less words are asked for than
    #are in the dictionary
    ({"cheese":1,"cheezits":4,"cheetos":7}, 2, {"cheetos":7,"cheezits":4})
    

    
]

instances_to_decimal_cases = [
    #check that the simplest case of the function works
    ({"cheese":1},{"cheese":1},1),
    #check that single word inputs always result in one
    ({"cheese":10101},{"cheese":1},10101),
    #check that a simple dictionary with multiple words with positive integer
    #values functions
    ({"cheese":1,"malt":2},{"cheese":1/3,"malt":2/3},3),
    #check that if the sum of the values of the dictionary is 0, then the
    #function returns an empty dictionary
    ({"cheese":0,"malt":0},{},0)


]

remove_most_common_cases = [
    #Check that a blank normal dictionary does not remove any words from the
    #gamer dictionary
    ({},{"game":.1,"gaming":.6,"poggers":.3},0,1 \
        ,{},{"game":.1,"gaming":.6,"poggers":.3},[]),
    
    #check a simple case where a word gets removed
    ({"game":.13},{"game":.1,"gaming":.7,"poggers":.5},1,1,\
        {},{"gaming":.7/1.2,"poggers":.5/1.2},["game"]),

    #check more complex case where some words get removed, some words are 
    #different in each dictionary and the total number of words in each 
    #dictionary is both not one and not the same
    ({"game":.13,"poggers":1,"gaming":.65,"soul":1},{"game":.1,"gaming":.7,"salmon":.4,"poggers":.6},3,4,\
        {"poggers":1/(1 + 1),"soul":1/(1 + 1)},{"salmon":.4/1,"poggers":.6/1},["game","gaming"]),




]

remove_too_uncommon_cases = [
    #test a simple case with clearly removable entries and a threshold equal to
    #one of the values of a key
   ({"gamers":1,"pasta":24,"notgamer":4,"gamingaminggaming":2},4,\
       {"pasta":24,"notgamer":4}),
    #test that keys of the form "wordcword" get removed
    ({"mochacmocha":101010101,"gamers":6,"aditicaditi":85,"lukecaditi":16,\
        "pastacpasta":2},3,{"gamers":6,"lukecaditi":16}),
    #check that overly long entries are removed
    ({"asfdljkasfdladsfjksfdakhasfdlfsda":110},2,{}),
    #check an empty dictionary
    ({},0,{})

    

]

determine_gamer_words_cases = [
    #check a simple case with a gamer word that is used drastically more in the
    #gamer dictionary than the normal dictionary
    ({"gaming":.01,"pogggg":.01},{"gaming":.1,"pogggg":.05},["gaming"]),
    #check that a gamer word that isn't in the normal dictionary makes the list
    ({"blame":.152},{"blame":.153,"sled":.000078,"sleigh":.00008},["sleigh"]),
    #check that a word that shows up a substantially different amount in the
    #normal and gamer dictionaries but is used less in the gamer dictionary is
    #not considered a gamer word
    ({"fantasy":1},{"fantasy":.000000000000001},[])
]

#the parse_words function is composed entirely of the previous functions and
#thus does not need unit tests, or rather the unit tests for this function 
#would fundamentally test the same things as the previous unit tests

determine_language_similarity_cases = [
    #check that an empty language dictionary outputs the sum of the squares
    #of the user dictionary
    ({},{"gaming":3,"gamers":4},5),
    #check that if the user and language dictionaries are the same that
    #the result is 0
    ({"gaming":3,"gamers":4},{"gaming":3,"gamers":4},0),
    #Check a case with words in both dictionaries but with with unequal values
    ({"gaming":2,"gamers":4},{"gaming":5,"gamers":8},5),

#the analyze_users_language function does not have any unit tests written for it
#because it requires a folder full of csv's to run, which would be ridiculous
#to create for unit tests. Also, nearly every component of this function is
#combinations of other functions that have unit tests, so we are confident that
#the inner workings of the function function as intended. The fact that we
#recieve usable and vizualizable data from this function has allowed us to
#be confident that it works.



]

is_gamer_cases = [
    # Check a single start codon.
  

]


# Define standard testing functions to check functions' outputs given certain
# inputs defined above.
@pytest.mark.parametrize("freq_input_dict,freq_input_int,output_dict", find_most_frequent_cases)
def test_find_most_frequent(freq_input_dict, freq_input_int, output_dict):
    """
    
    """
    assert find_most_frequent(freq_input_dict, freq_input_int) == output_dict


@pytest.mark.parametrize("input_dictionary,output_dictionary,total_words",
                         instances_to_decimal_cases)
def test_instances_to_decimal(input_dictionary, output_dictionary,total_words):
    """
    

    """
    assert instances_to_decimal(input_dictionary) == (output_dictionary,total_words)


@pytest.mark.parametrize("normal_dictionary,gamer_dictionary,normal_total_words,gamer_total_words,normal_dict_out,\
gamer_dict_out,ignore_list_out", remove_most_common_cases)
def test_remove_most_common(normal_dictionary, gamer_dictionary,normal_total_words,gamer_total_words,normal_dict_out,\
    gamer_dict_out,ignore_list_out):
    """

     """
    assert remove_most_common(normal_dictionary, gamer_dictionary,normal_total_words,gamer_total_words) == \
        (normal_dict_out,gamer_dict_out,ignore_list_out)

@pytest.mark.parametrize("dictionary,threshold,dictionary_out", remove_too_uncommon_cases)
def test_remove_too_uncommon(dictionary,threshold,dictionary_out ):
    """
    
    """
    assert remove_too_uncommon(dictionary,threshold) == dictionary_out


@pytest.mark.parametrize("normal_dictionary,gamer_dictionary,word_list", determine_gamer_words_cases)
def test_determine_gamer_words(normal_dictionary, gamer_dictionary,word_list):
    """
    
    """
    assert determine_gamer_words(normal_dictionary,gamer_dictionary) == word_list


@pytest.mark.parametrize("language_dict,user_dict,closeness_value", determine_language_similarity_cases)
def test_determine_language_similarity(language_dict, user_dict,closeness_value):
    """
    
    """
    assert determine_language_similarity(language_dict,user_dict) == closeness_value


@pytest.mark.parametrize("strand,orf", is_gamer_cases)
def test_is_gamer(strand, orf):
    """
    

    """
    assert is_gamer(strand) == orf

