from ..objects import Post, Question, Answer, User, Comment

from bs4 import BeautifulSoup

# TODO: Enhance the unittests here to be more thorough.
# TODO: Look into different forms of HTML in posts, such as lists etc.

def test_post_object():

    # Empty data dict.
    p = Post({})
    assert p.body == ''
    assert p.text == ''
    assert p.code == []
    assert p.soup == BeautifulSoup('')

    # Simple data dict
    d = {'body': '<p>bar</p><code>x=1</code><br/>'}
    p = Post(d)
    assert p.code == ['x=1']
    assert p.text == 'bar'
    assert p.text.words == ['bar']
    assert p.text.sentences == ['bar']

    # More complicated body example.
    d = {'body': '''<html>
                    <body>
                        <p>This is a long piece of code!</p>
                        <p>It contains multiple paragraphs, and some of them will even contain <code>code!</code></p>

                        <code>if code is code: print("code!")</code>
                    </body>
                    </html>'''}
    p = Post(d)
    assert p.code == ['code!', 'if code is code: print("code!")']
    assert p.text == 'This is a long piece of code!\nIt contains multiple paragraphs, and some of them will even contain'
    assert p.text.words == ['This', 'is', 'a', 'long', 'piece', 'of', 'code', '!', 'It', 'contains', 'multiple',
                            'paragraphs', ',', 'and', 'some', 'of', 'them', 'will', 'even', 'contain']
    assert p.text.sentences == ['This is a long piece of code!',
                                'It contains multiple paragraphs, and some of them will even contain']

    # Bold and italic text formatting.
    d = {'body':'<p>I like <b>different</b> <i>formatting!</i></p>'}
    p = Post(d)
    assert p.text == 'I like different formatting!'
    assert p.code == []
    assert p.text.words == ['I', 'like', 'different', 'formatting', '!']
    assert p.text.sentences == ['I like different formatting!']

    # Image link added
    d = {'body':'''<p>I like this image!</p>

         <p><img src=\"http://img-9gag-ftw.9cache.com/photo/aYpROWw_700b.jpg\" alt=\"Image description\"></p>'''}
    p = Post(d)
    assert p.text == 'I like this image!'
    assert p.code == []
    assert p.text.words == ['I', 'like', 'this', 'image', '!']
    assert p.text.sentences == ['I like this image!']

    # List testing
    s = '''<p>More specifically:</p>

           <ol>
           <li>What does <code>n=n</code> mean?</li>
           <li>What will be the content of <code>'list'</code>?</li>
           <li><p>What will be the output of </p>

           <p><code>print(list[0](14))</code> and <code>print(list[0]()(14))</code></p></li>
           </ol>

           <p>and why?</p>'''
    d = {'body':s}
    p = Post(d)
    assert p.text == ('More specifically:\n\n'
                      'What does  mean?\n'
                      'What will be the content of ?\n'
                      'What will be the output of \n'
                      ' and \n\n'
                      'and why?')
    assert p.code == ['n=n', "'list'", 'print(list[0](14))', 'print(list[0]()(14))']

def test_answer_object():
    d = {'body': '<p>bar</p><code>x=1</code>'}
    a = Answer(d)
    assert a.code == ['x=1']
    assert a.text == 'bar'


def test_comment_object():
    d = {'body': '<p>bar</p><code>x=1</code>'}
    c = Comment(d)
    assert c.code == ['x=1']
    assert c.text == 'bar'


def test_question_object():
    d = {'body': '<p>bar</p><code>x=1</code>'}
    q = Question(d, answers=[{'a': 1}])
    assert q.code == ['x=1']
    assert q.text == 'bar'
    assert q.answers != [Answer({'a': 1})]


# TODO: User object tests make no sense!
def test_user_object():
    d = {'body': '<p>bar</p><code>x=1</code>'}
    u = User(d)
    assert u._data == d
