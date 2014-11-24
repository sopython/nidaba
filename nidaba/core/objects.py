from pyparsing import makeHTMLTags, SkipTo
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """
    Simple parser to strip HTML tags.
    :param: None
    :return: None
    """

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


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
        self.body = self._data.get('Body', '')
        self.text = strip_tags(self.body)
        self.code = self._get_code(self.body)

        if answers is None:
            self.answers = []
        else:
            self.answers = [Answer(ans) for ans in answers]

        if comments is None:
            self.comments = []
        else:
            self.comments = [Comment(comm) for comm in comments]

    @classmethod
    def _get_code(cls, html):
        code_start, code_end = makeHTMLTags('code')
        code = code_start + SkipTo(code_end).setResultsName('body') + code_end
        return [token.body for token, start, end in code.scanString(html)]


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
