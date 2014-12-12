from ..objects import Post, Question, Answer, User, Comment

# TODO: Enhance the unittests here to be more thorough.

def test_post_object():
    d = {'Body': '<p>bar</p><code>x=1</code><br/>'}
    p = Post(d)
    assert p.code == ['x=1']
    assert p.text == 'bar'
    d = {'Body': '''<html>
                    <body>
                        <p>This is a long piece of code!</p>
                        <p>It contains multiple paragraphs, and some of them will even contain <code>code!</code></p>

                        <code>if code is code: print("code!")</code>
                    </body>
                    </html>'''}
    p = Post(d)
    assert p.code == ['code!', 'if code is code: print("code!")']
    assert p.text == 'This is a long piece of code!\nIt contains multiple paragraphs, and some of them will even contain'

    d = {'Body':'<p>I like <b>different</b> <i>formatting!</i></p>'}
    p = Post(d)
    assert p.text == 'I like different formatting!'

def test_answer_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    a = Answer(d)
    assert a.code == ['x=1']
    assert a.text == 'bar'


def test_comment_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    c = Comment(d)
    assert c.code == ['x=1']
    assert c.text == 'bar'


def test_question_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    q = Question(d, answers=[{'a': 1}])
    assert q.code == ['x=1']
    assert q.text == 'bar'
    assert q.answers != [Answer({'a': 1})]


# TODO: User object tests make no sense!
def test_user_object():
    d = {'Body': '<p>bar</p><code>x=1</code>'}
    u = User(d)
    assert u._data == d
