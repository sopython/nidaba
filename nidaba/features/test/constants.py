import json

question_filename = './data/test_question.json'
with open(question_filename, 'r') as f:
    example_question = json.loads(f.read())
    example_question_body = example_question['Body']

# answer_filename = './data/test_answer.json'
# with open(answer_filename, 'r') as f:
#     example_answer = json.loads(f.read())
