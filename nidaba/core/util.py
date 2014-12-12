from nltk import word_tokenize, sent_tokenize

class Text(str):
    @property
    def lower_text(self):
        return self.lower()

    @property
    def words(self):
        return word_tokenize(self)

    @property
    def sentences(self):
        return sent_tokenize(self)
