import sys

import pytest
from nidaba.features._util import question
from nidaba.exceptions import FeatureException

def test_get_weekday():
    """
    Test the get_weekday() _util function.
    :return: None
    """

    # Regular data
    assert question.get_weekday(1416654427) == 5
    assert question.get_weekday(1417000158) != 5

    # Ensure processes negative dates properly
    assert question.get_weekday(-100000000) == 0
    assert question.get_weekday(-99913600) != 0

    # Ensure that days tick over properly (and that UTC timezone is being used)
    assert question.get_weekday(345599) == 6
    assert question.get_weekday(345600) == 0

    with pytest.raises(Exception):
        raise Exception()

    with pytest.raises(FeatureException):
        question.get_weekday(sys.maxsize+1)  # Overflow Error

    with pytest.raises(FeatureException):
        question.get_weekday(-sys.maxsize-1)  # OSError

    with pytest.raises(FeatureException):
        max_date_epoch = 253402300799
        question.get_weekday(max_date_epoch+1)  # Value Error (31st December 9999 23:59:59)

    with pytest.raises(FeatureException):
        min_date_epoch = -253402300799
        question.get_weekday(min_date_epoch-1)


def test_is_weekend():
    """
    Test the is_weekend() _util function.
    :return: None
    """
    assert question.is_weekend(1416654427) is True
    assert question.is_weekend(1417000158) is False


def test_categorise_string_characters():
    """
    Test the categorise_string_characters() _util function
    :return: None
    """
    s = '''Cåbbage makes the \n world go round!!!!!1111ONE111!'''
    c = question.categorise_string_characters(s)

    assert isinstance(c, dict)
    assert c['Ll'] == 26  # Uppercase letters
    assert c['Lu'] == 4  # Lowercase letters
    assert c['Zs'] == 6  # Spaces
    assert c['Cc'] == 1  # Control chars (tabs, newlines, etc)

    assert not question.categorise_string_characters('')


def test_character_fractions():
    """
    Test the character_fractions() _util function.
    :return: None
    """

    s = '\n'.join(["Mae hen wlad fy nhadau yn annwyl i mi,",
                   "Gwlad beirdd a chantorion, enwogion o fri;",
                   "Ei gwrol ryfelwyr, gwladgarwyr tra mad,",
                   "Dros ryddid collasant eu gwaed."])
    result = question.character_fractions(s)

    assert result.upper == 4/153
    assert result.lower == 117/153
    assert result.numeric == 0
    assert result.punctuation == 6/153
    assert result.space == 23/153
    assert result.control == 3/153

    s = 'x = (6.63*10^-34)'
    result = question.character_fractions(s)

    assert result.numeric == 7/12
    assert result.punctuation == 2/12

    assert question.character_fractions('') == (0, 0, 0, 0, 0, 0)


def test_capitalised_string():
    """
    Test the capitalised_string() function.
    :return: None
    """
    assert question.capitalised_string('Why is reading lines from stdin much slower in C++ than Python?')
    assert not question.capitalised_string('how make pysmp oids respone readable for human')
    assert not question.capitalised_string('??? wat do???')


def test_string_length_fraction():
    """
    Test the string_length_fraction() function.
    :return: None
    """
    str1 = ['    x = 1    \n\n\n ', '              z = 2', ]
    str2 = ['i want\t \t ',  'o       ', ]
    assert question.string_length_fraction(str1, str2) == 0.5
    assert question.string_length_fraction(str1, str2) != 1.0


def test_stackoverflow_urls():
    """
    Test the stackoverflow_urls() function
    :return: None
    """

    # Empty dict that should be returned if no matches found
    empty = {'questions': [], 'answers': [], 'comments': [], 'users': []}

    assert question.stackoverflow_urls('') == empty  # Empty string
    assert question.stackoverflow_urls("some short sentence that\nreally shouldn't match") == empty  # No url
    assert question.stackoverflow_urls('I love http://www.google.co.uk') == empty  # Non-matching url
    assert question.stackoverflow_urls('http://stackoverflow.com/questions/tagged/python') == empty  # Non-matching SO url

    questions = ['http://stackoverflow.com/questions/27187789/python-regular-expressions-use-of-or',
                 'http://stackoverflow.com/q/27187776/3005188',
                 'http://stackoverflow.com/q/27187776/',
                 'http://stackoverflow.com/q/27187776',
                 'http://stackoverflow.com/questions/27187682']

    for s in questions:
        result = question.stackoverflow_urls(s)
        assert s in result['questions']
        for i in ['answers', 'comments', 'users']:
            assert s not in result[i]

    answers = ['http://stackoverflow.com/a/27190092/3005188',
               'http://stackoverflow.com/a/27190092/',
               'http://stackoverflow.com/a/27190092',
               'http://stackoverflow.com/questions/27190013/how-do-i-convert-32b-four-characters/27190092#27190092']

    for s in answers:
        result = question.stackoverflow_urls(s)
        assert s in result['answers']
        for i in ['questions', 'comments', 'users']:
            assert s not in result[i]

    comments = ['http://stackoverflow.com/questions/27189044/import-with-dot-name-in-python#comment42865341_27189110',
                'http://stackoverflow.com/questions/27189044/import-with-dot-name-in-python#comment42864835_27189044']

    for s in comments:
        result = question.stackoverflow_urls(s)
        assert s in result['comments']
        for i in ['questions', 'answers', 'users']:
            assert s not in result[i]

    users = ['http://stackoverflow.com/users/3005188/ffisegydd',
             'http://stackoverflow.com/users/100297/',
             'http://stackoverflow.com/users/100297']

    for s in users:
        result = question.stackoverflow_urls(s)
        assert s in result['users']
        for i in ['questions', 'comments', 'answers']:
            assert s not in result[i]

    # Testing a long string filled with multiple urls
    s = '''This is going to be a very long string. It is going to contain links to questions like
           http://stackoverflow.com/q/27187776/3005188. It's also going to contain links to some answers using html
           just like <a href="http://stackoverflow.com/a/27190092/3005188">this!</a>. It may even contain some comments
           if you're well behaved, like http://stackoverflow.com/questions/27189044/import-with-dot-name-in-python#comment42864835_27189044!

           It's been written by a particular user, you can find his profile at http://stackoverflow.com/users/3005188/ffisegydd.'''

    d = question.stackoverflow_urls(s)

    assert 'http://stackoverflow.com/q/27187776/3005188' in d['questions']
    assert 'http://stackoverflow.com/a/27190092/3005188' in d['answers']
    assert 'http://stackoverflow.com/questions/27189044/import-with-dot-name-in-python#comment42864835_27189044' in d['comments']
    assert 'http://stackoverflow.com/users/3005188/ffisegydd' in d['users']

    assert all(len(v) == 1 for k, v in d.items())  # Testing that only one url has been found for each key/value pair.

    # Testing multiple questions in the same string.
    d = question.stackoverflow_urls(' '.join(questions))

    assert len(d['questions']) == 5

def test_python_docs_urls():
    """
    Test python-docs_urls function which gets urls to Python documentation from a string
    :return: None
    """

    empty = []

    assert question.python_docs_urls('') == empty  # Empty string
    assert question.python_docs_urls("some short sentence that\nreally shouldn't match") == empty  # No url
    assert question.python_docs_urls('I love http://www.google.co.uk') == empty  # Non-matching url
    assert question.python_docs_urls('http://stackoverflow.com/questions/tagged/python') == empty  # Non-matching SO url

    # Various urls from docs.python.org that should all match
    urls = ['docs.python.org',
            'https://docs.python.org/3.2',
            'http://docs.python.org/3.3',
            'https://docs.python.org/3/index.html',
            'https://docs.python.org/3/whatsnew/3.4.html',
            'https://docs.python.org/3/library/functions.html',
            'https://docs.python.org/2.6/library/functions.html#eval',
            'https://docs.python.org/2.7/library/csv.html#csv.Error',
            'https://docs.python.org/3.5/',
            'https://docs.python.org/3/library/stdtypes.html#class.__mro__',
            'https://docs.python.org/3/c-api/init.html#c.Py_SetPath',
            'https://docs.python.org/dev/',
            'https://docs.python.org/3/library/xml.sax.reader.html#xml.sax.xmlreader.AttributesImpl',
            'https://docs.python.org/3/glossary.html#glossary',
            'https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.handle_expect_100']

    for url in urls:
        result = question.python_docs_urls(url)
        assert result[0] == url

    s = """This is going to be a very long string! I love the Python docs at https://docs.python.org. I particularly
           like the doc for https://docs.python.org/3/library/stdtypes.html#class.__mro__. Though you should also check
           what is new in Python 3.5 here https://docs.python.org/3.5/whatsnew/3.5.html"""

    result = question.python_docs_urls(s)

    urls = ['https://docs.python.org',
            'https://docs.python.org/3/library/stdtypes.html#class.__mro__',
            'https://docs.python.org/3.5/whatsnew/3.5.html']

    for url in urls:
        assert url in result
