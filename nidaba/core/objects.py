class Answer(object):
    """
    Stack Overflow Answer object which will hold information for use in Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing Answer information.
        :return: None
        """

        self.__data = data


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
            self.answers = []
        else:
            self.answers = [Answer(ans) for ans in answers]