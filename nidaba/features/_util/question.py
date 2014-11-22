from string import ascii_letters

import datetime


### General

def is_weekend(t):
    week_day = datetime.datetime.fromtimestamp(t).weekday()
    return week_day in (5, 6)

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
