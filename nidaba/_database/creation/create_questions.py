from pymongo import MongoClient
from lxml import etree
from dateutil.parser import parse

import pickle
from time import gmtime, strftime
import os.path
import os

data_dir = '../../so_data'
file_name = 'Posts.xml'
db_name = 'nidaba'
coll_name = 'questions'

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Id', 'PostTypeId', 'ParentId', 'Score', 'ViewCount',
              'OwnerUserId', 'AcceptedAnswerId', 'AnswerCount', 'CommentCount',
              'FavoriteCount', 'LastEditorUserId'}
str_to_date = {'CreationDate', 'LastActivityDate', 'LastEditDate',
               'CommunityOwnedDate', 'ClosedDate'}
str_to_list = {'Tags'}

def convert_tags(s):
    return [i.strip('<') for i in s.split('>')[:-1]]

f = open('./logs/{:s}.log'.format(coll_name), 'w')
s = 'Importing {:s} data.\n\n'.format(coll_name)
f.write(s)
print(s, end='')

i = 0
question_ids = set()

for event, elem in context:
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = {k:int(v) if k in str_to_int else
             parse(v) if k in str_to_date else
             convert_tags(v) if k in str_to_list else
             v for k, v in elem.items()}
        if d['PostTypeId'] == 1 and 'python' in d['Tags']:
            coll.insert(d)
            # Add the post id to a set for pickling. This will be used
            # in other creation files to only create answers/comments/etc
            # that belong to Python questions.
            question_ids.add(d['Id'])
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            i += 1
            if i % 1000 == 0:
                s_option = (strftime('%H:%M:%S', gmtime()), d['Id'])
                s = '{:s} : Id - {:d}\n'.format(*s_option)
                print(s, end='')
                f.write(s)

print('Finished importing, now creating indices.')

coll.ensure_index('Id')

f.close()

with open('question_ids.pickle', 'wb') as f:
    pickle.dump(question_ids, f)
