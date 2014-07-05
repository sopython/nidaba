from pymongo import MongoClient
from lxml import etree
from dateutil.parser import parse

from time import gmtime, strftime
import os.path
import os

data_dir = '../../so_data'
file_name = 'Users.xml'
db_name = 'nidaba'
coll_name = 'users'

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Views', 'UpVotes', 'DownVotes', 'AccountId', 
              'Age', 'Id', 'Reputation'}
str_to_date = {'CreationDate', 'LastAccessDate'}

f = open('./logs/{:s}.log'.format(coll_name), 'w')
f.write('Importing {:s} data.\n\n'.format(coll_name))

for i, (event, elem) in enumerate(context):
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = {k:int(v) if k in str_to_int else
             parse(v) if k in str_to_date else
             v for k, v in elem.items()}
        coll.insert(d)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        if i % 50000 == 0:
            s_option = (strftime('%H:%M:%S', gmtime()), d['Id'])
            s = '{:s} : Id - {:d}\n'.format(*s_option)
            print(s, end='')
            f.write(s)
            
coll.ensure_index('Id')

f.close()

