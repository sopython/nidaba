from bs4 import BeautifulSoup
import requests
import re
from stackpy import Site
from pymongo import MongoClient

common = requests.get('http://sopython.com/CommonQuestions').text
soup = BeautifulSoup(common)
db = MongoClient().stackoverflow.common

q_re = re.compile('q(?:uestions)?/(\d+)')
hrefs = soup.find_all('a', href=q_re)
q_ids = [q_re.search(tag['href']).group(1) for tag in hrefs]
questions = list(Site('stackoverflow').questions(q_ids))
for question in questions:
	question._data['category'] = []
	db.insert(question._data)



