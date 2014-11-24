from .._util import question


### General

def test_get_weekday():
    assert question.get_weekday(1416654427) == 5
    assert question.get_weekday(1417000158) != 5


def test_is_weekend():
    assert question.is_weekend(1416654427) is True
    assert question.is_weekend(1417000158) is False

### Title

def test_title_capitalisation():
    assert question.capitalised_title('Why is reading lines from stdin much slower in C++ than Python?')
    assert not question.capitalised_title('how make pysmp oids respone readable for human')
    assert not question.capitalised_title('??? wat do???')

def test_title_capitalisation_percentage():
    assert question.title_capitalisation_percentage('Why is reading lines from stdin much slower in C++ than Python?') == 3/(46 + 3)
    assert question.title_capitalisation_percentage('how make pysmp oids respone readable for human') == (0/(39 + 0))
    assert question.title_capitalisation_percentage('WAT DO PYTHON') == 11/(0 + 11)
    assert question.title_capitalisation_percentage('Matplotlib: I need SOME HELP!!!') == 10/(13 + 10)


### Body

def code_percentage():
    code = ['    x = 1    \n\n\n ', '              z = 2', ]
    text = ['i want\t \t ',  'o       ', ]
    assert question.code_percentage(code, text) == 0.5
    assert question.code_percentage(code, text) != 0.5

### Code

### Tags

### Answers

### Comments
