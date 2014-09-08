# -*- encoding: utf-8 -*-

import sys
from twisted.python import log
log.startLogging(sys.stdout)

from twisted.internet import reactor
from datetime import datetime
from autobahn.websocket import (
    WebSocketClientFactory,
    WebSocketClientProtocol,
    connectWS
)
import json
from bs4 import BeautifulSoup
import pymongo
from stackpy import Site

posts = pymongo.MongoClient().stackoverflow.posts

def do_something(jd):
    qid, tags, body = jd['data']['id'], jd['data']['tags'], BeautifulSoup(jd['data']['body'])    
    log.msg(u'{src} {dt} ({reason}): [{id} {status}] {title} - [{tags}].'.format(
        dt = body.select('.relativetime')[0]['title'],
        id = qid,
        title = body.select('div .summary h3 a')[0].text,
        status = u' '.join(body.select('.status')[0].attrs['class']),
        reason = body.select('.user-action-time')[0].text.strip(),
        tags = u' '.join(tags),
        src = jd['action']
    ))
    return jd['data']['id']

def do_something_else(jd):
    qid = jd['action'].rsplit('-', 1)[1]
    jd['data']['datetime_seen'] = datetime.now()
    posts.update({'_id':qid}, {'$push': {'timeline': jd['data']}})
    log.msg(u'[{id}] {data}'.format(id=qid, data=jd['data']))
    

class QuestionFeedProtocol(WebSocketClientProtocol): 
    def onOpen(self):        
        log.msg('Connected to questions websocket.')
        self.sendMessage('1-questions-active-tag-python*')
        log.msg('Streams requested.')
        self.seen = set()


    def onMessage(self, msg, binary):
        if binary:
            log.warning('Binary message ignored {!r}'.format(msg))
            return
        jd = json.loads(msg)
        jd['data'] = json.loads(jd['data'])
        if jd['action'].startswith('1-questions-active'):
            qid = do_something(jd)
            if qid not in self.seen:
                self.sendMessage('1-question-{}'.format(qid))
		try:
                qinfo = Site('stackoverflow').questions(qid).filter('withbody')[0]._data                
	            qinfo['_id'] = qid
        	    qinfo['datetime_seen'] = datetime.now()
                posts.insert(qinfo)
                self.seen.add(qid)
		except Exception:
			pass
        else:
            do_something_else(jd)


if __name__ == '__main__':
    factory = WebSocketClientFactory("ws://sockets.ny.stackexchange.com", debug=False)
    factory.protocol = QuestionFeedProtocol
    connectWS(factory)
    reactor.run()
