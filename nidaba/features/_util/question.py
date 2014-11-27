import datetime
from unicodedata import category
from collections import Counter, namedtuple, OrderedDict


def get_weekday(t):
    """
    Returns the day of the week.
    :param t: Timestamp
    :return: Integer corresponding to day of the week 0-6 for Mon-Sun.
    """
    return datetime.datetime.fromtimestamp(t).weekday()


def is_weekend(t):
    """
    Returns True if the argument occurs on a weekend.
    :param t: Timestamp
    :return: True if weekend else False.
    """
    return get_weekday(t) in (5, 6)


def capitalised_string(s):
    """
    Check whether the first letter of a title is uppercase
    :param s: String containing a title.
    :return: True if first letter is uppercase else False.
    """
    try:
        return s[0].isupper()
    except IndexError:
        return False


def categorise_string_characters(s):
    """
    Calculates the category of each letter and returns the count. Categories are defined at http://www.unicode.org/reports/tr44/tr44-6.html
    but the following ones are the most common:
    - Lu : Lowercase letter
    - Ll : Uppercase letter
    - Nd : Decimal number
    - Po : Other punctuation
    - Zs : Space separator

    :param s: Input string to be counted.
    :return: Counter (dict) full of the category counts.
    """

    c = Counter(category(i) for i in s)

    return c


def character_fractions(s):
    """
    Calculate the fraction that various categories of character take, with respect to the sum of the whole.

    This function does not currently support every single category. Missing categories include: brackets, hyphens, math symbols.
    These missing categories can be added, if necessary, by simply adding to the categories OrderedDict.
    :param s: Input string
    :return: namedtuple with various fractions
    """

    categories = OrderedDict([('upper', 'Lu'),
                              ('lower', 'Ll'),
                              ('numeric', 'Nd'),
                              ('punctuation', 'Po'),
                              ('space', 'Zs'),
                              ('control', 'Cc')])

    Fraction = namedtuple('Fraction', categories.keys())

    c = categorise_string_characters(s)

    total = sum(v for k, v in c.items() if k in categories.values())
    print(total)
    if total == 0:
        return Fraction(*[0]*len(categories))  # Dirty hack is dirty. I love it.

    fraction = Fraction(*[c[v]/total for k, v in categories.items()])

    return fraction


def string_length_fraction(str_list_1, str_list_2):
    """
    Calculate the percentage difference in length between two strings, such that s1 / (s1 + s2)
    :param str_list_1: List of strings.
    :param str_list_2: List of strings.
    :return: Float (0 to 1).
    """
    str1_size = sum(sum(len(j.strip()) for j in i) for i in str_list_1)
    str2_size = sum(sum(len(j.strip()) for j in i) for i in str_list_2)

    return str1_size/(str1_size + str2_size)
