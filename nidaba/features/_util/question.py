import datetime
import re
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


def stackoverflow_urls(s):
    """
    Return any urls that belong to Stack Overflow.
    :param s: Input string to get urls from.
    :return: dict with stackoverflow urls, keys are 'question', 'answer',
             etc and the values are lists of url strings.
    """

    flags = re.IGNORECASE

    base = r'(?:https?://)?(?:www\.)?stackoverflow\.com/'
    q_string = r'({}q(?:uestions)?/(?:\d+)(?:/[\w-]+)?/?)'
    a_string = r'({}(?:questions/(?:\d+)/[\w-]*?/(?:\d+)(?:#\S+)?|a/(?:\d+)?/?(?:\d+)?))'
    c_string = r'({}q(?:uestions)?/(?:\d+)(?:/[\w-]+)?#comment(?:\d+)_(?:\d+))'
    u_string = r'({}u(?:sers)?/(?:\d+)/?(?:\w+)?)'

    q_regex = re.compile(q_string.format(base), flags)
    a_regex = re.compile(a_string.format(base), flags)
    c_regex = re.compile(c_string.format(base), flags)
    u_regex = re.compile(u_string.format(base), flags)

    # Have to be ran in a certain order to add the beginning index of the comments and answers urls.
    # Otherwise the questions url will match them accidentally. As such, we add the starting index
    # of each match object to a set. Then, if a question accidentally matches a comment url,
    # it isn't added because the starting index is already in the set.

    matches = set()

    regexes = [('users', u_regex),
               ('comments', c_regex),
               ('answers', a_regex),
               ('questions', q_regex)]

    result = {}

    for key, regex in regexes:
        result[key] = []
        for m in regex.finditer(s):
            if m.start(0) not in matches:
                result[key].append(m.group(0))
                matches.add(m.start(0))

    return result


def python_docs_urls(s):
    """
    Find urls that match the Python docs inside a string.
    :param s: Input string
    :return: List of urls
    """

    flags = re.IGNORECASE
    pattern = r"(?:https?://)?docs.python.org/?(?:\d+(?:\.(?:\d+|x))*)?/?(?:\w+(?:[.-]\w+)*)?/?(?:\w+(?:[.-]\w+)*)?#?[\w\-]*(?:\.[\w\-]+)*"
    regex = re.compile(pattern, flags)

    result = regex.findall(s)

    return result


def get_emoticons(text):
    """
    Return a dictionary of emoticons & their count in the given text.
    :param text: String or List of words.
    :return: Dictionary - emoticons as keys and their count as values.
    """
    emoticons = (":-) :) :D :o) :] :3 :c) :> =] 8) =) :} :^) :っ) :-D 8-D 8D"
                 "x-D xD X-D XD =-D =D =-3 =3 B^D :-)) >:[ :-( :( :-c :c :-<"
                 ":っC :< :-[ :[ :{ ;( :-|| :@  >:( :'-( :'(  :'-) :')D :< D:"
                 "D8 D; D= DX v.v D-': >:O :-O:O:-o:o 8-0 O_O o-o O_o o_O o_o"
                 "O-O :* :^* ;^) :-, >:P :-P :P X-P x-p xp XP :-p :p =p :-Þ"
                 ">:\ >:/ :-/ :-. :/ :\ =/ =\ :L =L :S >.< :| :-| :$ :-X :X"
                 ":-# :# O:-) 0:-3 0:3 0:-) 0:) 0;^) >:) >;) >:-) }:-) }:)"
                 "3:-) 3:) o/\o ^5 >_>^ ^<_< |;-) |-O :-J :-& :& #-) %-) %)"
                 ":-###.. :###.. <:-| ಠ_ಠ <*)))-{ ><(((*> ><> \o/ *\0/*"
                 "@}-;-'--- @>-->-- ~(_8^(I) 5:-) ~:-\ //0-0\\ *<|:-) =:o]"
                 ",:-) 7:^] <3 </3").split()
    if isinstance(text, str):
        text = text.split()
    return Counter(word for word in text if word in emoticons)
