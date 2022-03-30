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
    parse_words,
    determine_language_similarity,
    analyze_users_language,
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
    ({"cheese":1},{"cheese":1}),
    #check that single word inputs always result in one
    ({"cheese":10101},{"cheese":1}),
    #check that a simple dictionary with multiple words with positive integer
    #values functions
    ({"cheese":1,"malt":2},{"cheese":1/3,"malt":2/3}),
    #check that if the sum of the values of the dictionary is 0, then the
    #function returns an empty dictionary
    ({"cheese":0,"malt":0},{})


]

remove_most_common_cases = [
    #Check that a blank normal dictionary does not remove any words from the
    #gamer dictionary
    ({},{"game":.1,"gaming":.6,"poggers":.3},{},{"game":.1,"gaming":.6,"poggers":.3}\
        ,[]),
    ({"game":.13},{"game":.1,"gaming":.6,"poggers":.3},{},{"gaming":.6,"poggers":.3}\
        ,[]),


]

# remove_too_uncommon_cases = [
   

# ]

# determine_gamer_words_cases = [
  
# ]

# parse_words_cases = [
#     # Test a short strand starting with a start codon whose reverse complement
   
# ]

# determine_language_similarity_cases = [
#     # An ORF covering the whole strand is by default the longest ORF.
  

# ]

# analyze_users_language_cases = [
#     # Check a single start codon.
  

# ]


# # Define additional testing lists and functions that check other properties of
# # functions in gene_finder.py.
# @pytest.mark.parametrize("nucleotide", ["A", "T", "C", "G"])
# def test_double_complement(nucleotide):
#     """
#     Check that taking the complement of a complement of a nucleotide produces
#     the original nucleotide.

#     Args:
#         nucleotide: A single-character string representing one of the four DNA
#             nucleotides.
#     """
#     assert get_complement(get_complement(nucleotide)) == nucleotide


################################################################################
# Don't change anything below these lines.
################################################################################


# Define standard testing functions to check functions' outputs given certain
# inputs defined above.
@pytest.mark.parametrize("freq_input_dict,freq_input_int,output_dict", find_most_frequent_cases)
def test_find_most_frequent(freq_input_dict, freq_input_int, output_dict):
    """
    Test that each nucleotide is mapped to its correct complement.

    Given a single-character string representing a nucleotide that is "A", "T",
    "G", or "C", check that the get_complement function correctly maps the
    string to a single-character string representing the nucleotide's complement
    (also "A", "T", "G", or "C").

    Args:
        nucleotide: A single-character string equal to "A", "C", "T", or "G"
            representing a nucleotide.
        complement: A single-character string equal to "A", "C", "T", or "G"
            representing the expected complement of nucleotide.
    """
    assert find_most_frequent(freq_input_dict, freq_input_int) == output_dict


@pytest.mark.parametrize("input_dictionary,output_dictionary",
                         instances_to_decimal_cases)
def test_instances_to_decimal(input_dictionary, output_dictionary):
    """
    Test that a string of nucleotides get mapped to its reverse complement.

    Check that given a string consisting of "A", "C", "T", and "G" that
    represents a strand of DNA, the get_reverse_complement function correctly
    returns the reverse complement of the string, defined as the complement of
    each nucleotide in the strand in reverse order.

    Args:
        strand: A string consisting only of the characters "A", "C", "T", and
            "G" representing a strand of DNA.
        reverse_complement: A string representing the expected reverse
            complement of strand.
    """
    assert instances_to_decimal(input_dictionary) == output_dictionary


@pytest.mark.parametrize("normal_dictionary,gamer_dictionary,normal_dict_out,\
gamer_dict_out,ignore_list_out", remove_most_common_cases)
def test_remove_most_common(normal_dictionary, gamer_dictionary,normal_dict_out,\
    gamer_dict_out,ignore_list_out):
    """
#     """
    assert remove_most_common(normal_dictionary, gamer_dictionary) == \
        (normal_dict_out,gamer_dict_out,ignore_list_out)

# @pytest.mark.parametrize("strand,orfs", find_all_orfs_one_frame_cases)
# def test_find_all_orfs_oneframe(strand, orfs):
#     """
#     Test that a string representing a strand of DNA gets mapped to a list of all
#     non-overlapping open reading frames (ORFs) aligned to its frame.

#     Check that given a string representing a strand of DNA as defined above, the
#     find_all_orfs_oneframe function returns a list of strings representing all
#     non-overlapping ORFs in the strand that are aligned to the strand's frame
#     (i.e., starting a multiple of 3 nucleotides from the start of the strand).
#     Each ORF is a strand of DNA from a START codon to a STOP codon (or in the
#     case of the last ORF in the strand, to the end of the strand if no STOP
#     codon is encountered during reading).

#     Args:
#         strand: A string representing a strand of DNA.
#         orfs: A list of strings representing the expected strands of DNA that
#             are ORFs within strand's frame.
#     """
#     assert Counter(find_all_orfs_one_frame(strand)) == Counter(orfs)


# @pytest.mark.parametrize("strand,orfs", find_all_orfs_cases)
# def test_find_all_orfs(strand, orfs):
#     """
#     Test that a string representing a strand of DNA gets mapped to a list of all
#     open reading frames within the strand, with no overlapping ORFs within any
#     given frame of the strand.

#     Check that given a string representing a strand of DNA as defined above, the
#     find_all_orfs function returns a list of strings representing all ORFs in
#     the strand as defined above. Overlapping ORFs are allowed as long as they do
#     not occur in different frames (i.e., each ORF is only non-overlapping with
#     the other ORFs in its own frame).

#     Args:
#         strand: A string representing a strand of DNA.
#         orfs: A list of strings representing the expected strands of DNA that
#             are ORFs within strand, with no overlapping ORFs within one frame of
#             strand.
#     """
#     assert Counter(find_all_orfs(strand)) == Counter(orfs)


# @pytest.mark.parametrize("strand,orfs", find_all_orfs_both_strands_cases)
# def test_find_all_orfs_both_strands(strand, orfs):
#     """
#     Test that a string representing a strand of DNA gets mapped to a list of
#     all open reading frames within the strand or its reverse complement, with no
#     overlapping ORFs within a given frame.

#     Check that given a string representing a strand of DNA as defined above, the
#     find_all_orfs_both_strands function returns a list of strings representing
#     all ORFs in the strand or its reverse complement as defined above.

#     Args:
#         strand: A string representing a strand of DNA.
#         orfs: A list of strings representing the expected strands of DNA that
#             are ORFs within strand or its reverse complement, with no
#             overlapping ORFs within one frame of either.
#     """
#     assert Counter(find_all_orfs_both_strands(strand)) == Counter(orfs)


# @pytest.mark.parametrize("strand,orf", find_longest_orf_cases)
# def test_find_longest_orf(strand, orf):
#     """
#     Test that a string representing a strand of DNA gets mapped to a string
#     representing the longest ORF within the strand or its reverse complement.

#     Check that given a string representing a strand of DNA as defined above, the
#     find_longest_orf function returns a string representing a strand of DNA
#     equal to the longest ORF within the strand or its reverse complement.

#     Args:
#         strand: A string representing a strand of DNA.
#         orf: A string representing a strand of DNA equal to the expected longest
#             ORF in strand or its reverse complement.
#     """
#     assert find_longest_orf(strand) == orf


# @pytest.mark.parametrize("strand,protein", encode_amino_acids_cases)
# def test_encode_amino_acids(strand, protein):
#     """
#     Test that a string representing a strand of DNA gets mapped to a string
#     representing the amino acids encoded by the strand.

#     Check that given a string representing a strand of DNA as defined above, the
#     encode_amino_acids function returns a string consisting of one-letter IUPAC
#     amino acid codes corresponding to the sequence amino acids encoded by the
#     strand.

#     Args:
#         strand: A string representing a strand of DNA.
#         protein: A string representing the expected sequence one-letter IUPAC
#             amino acid codes encoded by strand.
#     """
#     assert encode_amino_acids(strand) == protein
