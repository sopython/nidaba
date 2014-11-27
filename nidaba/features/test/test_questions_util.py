from .._util import question


def test_get_weekday():
    """
    Test the get_weekday() _util function.
    :return: None
    """
    assert question.get_weekday(1416654427) == 5
    assert question.get_weekday(1417000158) != 5


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
