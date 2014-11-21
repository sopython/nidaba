"""Question class"""

class Question(object):
    """Stack Overflow Question object.

    Object to hold SO Question information for use in Nidaba analysis.
    """

    def __init__(self, data, answers=None):

        self.__data = data

        if answers is None:
            self.answers = []
        else:
            self.answers = answers