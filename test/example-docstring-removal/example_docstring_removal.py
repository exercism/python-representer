""" This module helps little sister with her vocabulary homework.

    And this is a multi-line module level docstring. It should be
    removed when the representation is processed.
 """


def add_prefix_un(word):
    """

    :param word: str of a root word
    :return:  str of root word with un prefix

    This function takes `word` as a parameter and
    returns a new word with an 'un' prefix.
    """
    return 'un' + word


def make_word_groups(vocab_words):
    """

    :param vocab_words: list of vocabulary words with a prefix.
    :return: str of prefix followed by vocabulary words with
             prefix applied, separated by ' :: '.

    This function takes a `vocab_words` list and returns a string
    with the prefix  and the words with prefix applied, separated
     by ' :: '.
    """

    multi_line_string = """This is a multi-line string.
    This should NOT get cleaned as a docstring, but retained, because it is assigned
    a name, and is therefore a plain string, and not a docstring."""

    return (" :: " + vocab_words[0]).join(vocab_words)


def remove_suffix_ness(word):
    """

    :param word: str of word to remove suffix from.
    :return: str of word with suffix removed & spelling adjusted.

    This function takes in a word and returns the base word with `ness` removed.
    """

    MULTI_LINE_CONSTANT = """This is a multi-line string constant.
       This should NOT get cleaned as a docstring, but retained, because it is assigned
       a name, and is therefore a plain string, and not a docstring."""

    return word[:-4] if word[-5] != 'i' else word[:-5] + 'y'


def adjective_to_verb(sentence, index):
    """

    :param sentence: str that uses the word in sentence
    :param index:  index of the word to remove and transform
    :return:  str word that changes the extracted adjective to a verb.

    A function takes a `sentence` using the
    vocabulary word, and the `index` of the word once that sentence
    is split apart.  The function should return the extracted
    adjective as a verb.
    """
    return sentence.split()[index].strip(".") + 'en'