from ..objects import Post, Question, Answer, User, Comment


def test_post_object():
    d = {'Body': '<p>bar</p><code>x=1</code><br/>'}
    p = Post(d)
    assert p.code == ['x=1']
    assert p.text == ['bar']


def test_answer_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    a = Answer(d)
    assert a.code == ['x=1']
    assert a.text == ['bar']


def test_comment_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    c = Comment(d)
    assert c.code == ['x=1']
    assert c.text == ['bar']


def test_question_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    q = Question(d, answers=[{'a': 1}])
    assert q.code == ['x=1']
    assert q.text == ['bar']
    assert q.answers != [Answer({'a': 1})]


def test_user_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    u = User(d)
    assert u._data == d
