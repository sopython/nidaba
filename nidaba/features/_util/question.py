from __future__ import division

from string import ascii_letters

import datetime


### General

def get_weekday(t):
    return datetime.datetime.fromtimestamp(t).weekday()

def is_weekend(t):
    return get_weekday(t) in (5, 6)

### Title

def capitalised_title(s):
    return s[0].isupper()

def title_capitalisation_percentage(s):
    upper = sum(i.isupper() for i in s)
    lower = sum(i.islower() for i in s)

    total = upper + lower

    return upper/total

### Body

### Code

### Tags

### Answers

### Comments
