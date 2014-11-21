from string import ascii_letters

### General

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