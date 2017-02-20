#!/usr/bin/python
# coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cobe.brain import Brain
import re
import urllib
import random

PORT_NUMBER = 8090

brain = Brain("adventure")

def unescape(s):
    return urllib.unquote_plus(s.encode('utf-8'))


def generate_jsonp(reply, user_id):
    return '''
    console.log('SanBot Server sending back JSONP')
    setTimeout(function(x, id) {
       post(x, id);
    }, 3000, "''' + re.escape(reply) + '\\\n' + '", ' + user_id + ');'


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        message = unescape(self.path).split('/')
        messageo = message[1].split(' ')
        messageo = ' '.join((i for i in messageo if not i.startswith('@')))
        untagged_reply = ' '.join((i for i in brain.reply(messageo).split(' ') if not i.startswith('@')))
        if random.random() < 0.95:
            reply = untagged_reply
        else:
            reply = untagged_reply + "\nDON'T BAN ME"
        user_id = message[2].decode(encoding="utf-8")
        # print(messageo.decode(encoding='utf-8') + '\t\t' + untagged_reply.decode())
        to_send = generate_jsonp(reply, user_id)
        self.wfile.write(to_send.encode(encoding="utf-8"))
        brain.learn(messageo)
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ' + str(PORT_NUMBER))

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
