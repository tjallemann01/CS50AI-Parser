import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# NONTERMINALS = """
# S -> N V
# """


NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det Nom | NP PP
Nom -> N | Adj Nom
VP -> V | V NP | V PP | V Adv
VP -> V NP PP | V PP Adv
VP -> VP PP | VP Adv | Adv VP
VP -> VP Conj VP
PP -> P NP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))



def preprocess(sentence):
    """
    Convert sentence into a list of lowercase words.
    Remove tokens that contain no alphabetic characters.
    """

    # Convert the sentence to lowercase.
    sentence = sentence.lower()

    # Tokenize the sentence using NLTK.
    tokens = nltk.word_tokenize(sentence)

    # Keep tokens containing at least one letter.
    words = []

    for token in tokens:
        if any(character.isalpha() for character in token):
            words.append(token)

    return words



def np_chunk(tree):
    """
    Return a list of noun phrase chunks in the sentence tree.

    A noun phrase chunk is an NP subtree that does not
    contain any other NP subtree within it.
    """

    chunks = []

    # Explore every subtree in the syntax tree.
    for subtree in tree.subtrees():

        # Consider only noun phrase subtrees.
        if subtree.label() != "NP":
            continue

        # Check whether this NP contains another NP.
        contains_nested_np = any(
            nested.label() == "NP"
            for nested in subtree.subtrees()
            if nested is not subtree
        )

        # Save only noun phrases without nested NPs.
        if not contains_nested_np:
            chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
