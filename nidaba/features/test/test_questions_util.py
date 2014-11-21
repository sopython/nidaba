from .fixtures import question_fixture
from .._util import question

### General

### Title

def test_title_capitalisation(question_fixture):
    assert question.capitalised_title(question_fixture['Title'])

def test_title_capitalisation_ratio(question_fixture):
    assert question.title_capitalisation_ratio(question_fixture['Title']) == (3./46.)

### Body

### Code

### Tags

### Answers

### Comments