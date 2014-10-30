import asyncio
from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json
from pprint import pprint

class StackActivity(WebSocketClientProtocol):

   def onConnect(self, response):
      # signal elsewhere later
      print('Connected:', response.peer)

   def onOpen(self):
      # request SO questions
      # (use 155-questions-active) for ALL SE sites)
      # (also should be able to put '1-questions-active-tag-python*' or similar)
      self.sendMessage(b'1-questions-active')
      # ^^^ might want to `call_later` this for a few seconds...

   def onMessage(self, payload, is_binary):
      # not sure if binary should technically happen?
      if not is_binary:
         event = json.loads(payload.decode('utf-8'))
         data = json.loads(event['data'])
         # it's a question, so subscribe to its events...
         if event['action'] == '1-questions-active':            
            self.sendMessage('1-question-{}'.format(data['id']).encode('utf-8'))
         pprint(data)

   def onClose(self, was_clean, code, reason):
      print('Closed:', reason)


factory = WebSocketClientFactory('ws://qa.sockets.stackexchange.com')
factory.protocol = StackActivity

loop = asyncio.get_event_loop()
coro = loop.create_connection(factory, 'qa.sockets.stackexchange.com', 80)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
