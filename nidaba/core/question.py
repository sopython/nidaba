from .answer import Answer

class Question(object):
    """
    Stack Overflow Question object which will hold information for use in Nidaba analysis
    """

    def __init__(self, data, answers=None):
        """
        :param data: dict containing Question information.
        :param answers: list of dicts containing answer information.
        :return: None
        """

        self.__data = data

        if answers is None:
            self.answers = [Answer(ans) for ans in answers]
        else:
            self.answers = answers