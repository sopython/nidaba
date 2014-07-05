from pymongo import MongoClient
from lxml import etree
from dateutil.parser import parse

import pickle
from time import gmtime, strftime
import os.path
import os

data_dir = '../../so_data'
file_name = 'PostLinks.xml'
db_name = 'nidaba'
coll_name = 'post_links'

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Id', 'PostId', 'RelatedPostId', 'LinkTypeId'}
str_to_date = {'CreationDate'}

# Load in a set of python ids.
with open('question_ids.pickle', 'rb') as q, \
     open('answer_ids.pickle', 'rb') as a:
    question_ids = pickle.load(q)
    answer_ids = pickle.load(a)
    ids = question_ids | answer_ids

f = open('./logs/{:s}.log'.format(coll_name), 'w')
s = 'Importing {:s} data.\n\n'.format(coll_name)
f.write(s)
print(s, end='')

i = 0
for event, elem in context:
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = dict(elem.items())
        if int(d['PostId']) in ids or int(d['RelatedPostId']) in ids:
            d = {k:int(v) if k in str_to_int else
                 parse(v) if k in str_to_date else
                 v for k, v in d.items()}
            coll.insert(d)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            i += 1
            if i % 10000 == 0:
                s_option = (strftime('%H:%M:%S', gmtime()), d['Id'], i)
                s = '{:s} : Id - {:d} : # - {:d}\n'.format(*s_option)
                print(s, end='')
                f.write(s)

print('Creating indices.')

coll.ensure_index('Id')

f.close()
