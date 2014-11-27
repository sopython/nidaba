from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


class SEObject(object):
    """
    Base Object for SE Objects
    """
    def __init__(self, data):
        self._data = data


class User(SEObject):
    """
    Stack Overflow User object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing user information.
        :return: None
        """
        super().__init__(data)


class Post(SEObject):
    """
    Base object for Question, Answer, Comments
    """

    def __init__(self, data):
        """
        :param data: Dict containing comment information.
        :return: None
        """
        super().__init__(data)
        self.body = self._data.get('Body', '')
        self.text = self._get_text(self.body)
        self.code = self._get_code(self.body)
        self.markup = self._get_markup(self.body)

    @classmethod
    def _get_code(cls, html):
        """
        Extract code without markup tags from a given html content.
        :param html: String
        :return List of code strings in the given content
        """
        return [i.get_text() for i in BeautifulSoup(html).find_all('code')]

    @classmethod
    def _get_text(cls, html):
        """
        Extract text from html content by removing markup tags & code.
        :param html: String
        :return List of strings in the given content
        """
        soup = BeautifulSoup(html)
        [s.extract() for s in soup('code')]
        return [i for i in soup.recursiveChildGenerator()
                if isinstance(i, NavigableString)]

    @classmethod
    def _get_markup(cls, html):
        """
        Filter markup tags from a given html content.
        :param html: String
        :return List of markup tags in the given content
        """
        soup = BeautifulSoup(html).recursiveChildGenerator()
        tags = [tag for tag in soup if isinstance(tag, Tag)]
        return [str(t) if t.isSelfClosing else str(t).replace(t.string, '')
                for t in tags]


class Comment(Post):
    """
    Stack Overflow Comment object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: Dict containing comment information.
        :return: None
        """
        super().__init__(data)


class Answer(Post):
    """
    Stack Overflow Answer object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing answer information.
        :return: None
        """
        super().__init__(data)


class Question(Post):
    """
    Stack Overflow Question object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data, answers=None, comments=None):
        """
        :param data: Dict containing question information.
        :param answers: List of dicts containing answer information.
        :param comments: List of dicts containing comment information
        :return: None
        """
        super().__init__(data)

        if answers is None:
            self.answers = []
        else:
            self.answers = [Answer(ans) for ans in answers]

        if comments is None:
            self.comments = []
        else:
            self.comments = [Comment(comm) for comm in comments]
