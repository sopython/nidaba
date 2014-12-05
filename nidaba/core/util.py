from nltk import word_tokenize, sent_tokenize

class Text(str):
    """
    Text object to hold non-code text.

    Subclassed from str with some extra methods for tokenisation.
    """

    @property
    def words(self):
        return word_tokenize(self)

    @property
    def sentences(self):
        return sent_tokenize(self)
