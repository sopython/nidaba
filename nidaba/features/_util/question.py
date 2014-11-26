from string import ascii_letters

import datetime


### General

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

### Title

def capitalised_title(s):
    """
    Check whether the first letter of a title is uppercase
    :param s: String containing a title.
    :return: True if first letter is uppercase else False.
    """
    return s[0].isupper()

def title_capitalisation_percentage(s):
    """
    Work out the percentage of characters which are uppercase, such that
    perc = upper / (upper+lower).
    :param s: String.
    :return: Float (0 to 1).
    """
    upper = sum(i.isupper() for i in s)
    lower = sum(i.islower() for i in s)

    total = upper + lower

    return upper/total

### Body


def string_length_percentage(str_list_1, str_list_2):
    """
    Calculate the percentage difference in length between two strings, such
    that s1 / (s1 + s2)
    :param str_list_1: List of strings.
    :param str_list_2: List of strings.
    :return: Float (0 to 1).
    """
    str1_size = sum(sum(len(j.strip()) for j in i) for i in str_list_1)
    str2_size = sum(sum(len(j.strip()) for j in i) for i in str_list_2)

    return str1_size/(str1_size + str2_size)

### Code

### Tags

### Answers

### Comments
