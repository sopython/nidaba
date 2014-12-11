from nltk import word_tokenize, sent_tokenize

class Text(object):

    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def lower_text(self):
        return self._text.lower()

    @property
    def words(self):
        return word_tokenize(self._text)
    
    @property
    def sentences(self):
        return sent_tokenize(self._text)
