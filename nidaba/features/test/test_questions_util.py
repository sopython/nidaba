from .._util import question

### General

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

### Code

### Tags

### Answers

### Comments