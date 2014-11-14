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
coll_name = 'answers'

# Load in a set of python question ids.
with open('question_ids.pickle', 'rb') as f:
    question_ids = pickle.load(f)

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Id', 'PostTypeId', 'ParentId', 'Score', 'ViewCount',
              'OwnerUserId', 'AcceptedAnswerId', 'CommentCount',
              'FavoriteCount', 'LastEditorUserId'}
str_to_date = {'CreationDate', 'LastActivityDate', 'LastEditDate',
               'CommunityOwnedDate', 'ClosedDate'}

f = open('./logs/{:s}.log'.format(coll_name), 'w')
s = 'Importing {:s} data.\n\n'.format(coll_name)
f.write(s)
print(s, end='')

i = 0
answer_ids = set()

for event, elem in context:
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = dict(elem.items())
        if int(d['PostTypeId']) == 2 and int(d['ParentId']) in question_ids:
            d = {k:int(v) if k in str_to_int else
                 parse(v) if k in str_to_date else
                 v for k, v in d.items()}
            coll.insert(d)
            answer_ids.add(d['Id'])
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            i += 1
            if i % 1000 == 0:
                s_option = (strftime('%H:%M:%S', gmtime()), d['Id'])
                s = '{:s} : Id - {:d}\n'.format(*s_option)
                print(s, end='')
                f.write(s)

coll.ensure_index('Id')

f.close()

with open('answer_ids.pickle', 'wb') as f:
    pickle.dump(answer_ids, f)

