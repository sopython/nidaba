class Comment(object):
    """
    Stack Overflow Comment object which will hold information for use in Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: Dict containing comment information.
        :return: None
        """

        self._data = data


class Answer(object):
    """
    Stack Overflow Answer object which will hold information for use in Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing answer information.
        :return: None
        """

        self._data = data


class Question(object):
    """
    Stack Overflow Question object which will hold information for use in Nidaba analysis
    """

    def __init__(self, data, answers=None, comments=None):
        """
        :param data: Dict containing question information.
        :param answers: List of dicts containing answer information.
        :param comments: List of dicts containing comment information
        :return: None
        """

        self._data = data

        if answers is None:
            self.answers = []
        else:
            self.answers = [Answer(ans) for ans in answers]

        if comments is None:
            self.comments = []
        else:
            self.comments = [Comment(comm) for comm in comments]


class User(object):
    """
    Stack Overflow User object which will hold information for use in Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing user information.
        :return: None
        """

        self._data = data
