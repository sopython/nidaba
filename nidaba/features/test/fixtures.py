import pytest

import json

@pytest.fixture
def question_fixture(scope='module'):
    """Question fixture giving access to question data in dict form."""
    question_filename = './data/test_question.json'

    with open(question_filename, 'r') as f:
        q = json.loads(f.read())

    return q

@pytest.fixture
def answer_fixture(scope='module'):
    """Answer fixture giving access to question data in dict form."""
    answer_filename = './data/test_answer.json'

    with open(answer_filename, 'r') as f:
        a = json.loads(f.read())

    return a

@pytest.fixture
def user_fixture(scope='module'):
    """Answer fixture giving access to question data in dict form."""
    user_filename = './data/test_user.json'

    with open(user_filename, 'r') as f:
        a = json.loads(f)

    return u
