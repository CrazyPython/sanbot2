class StackExchangeWeb(object):
    PORT_NUMBER = 8090

    def __init__(self, bot, start=True):
        self.bot = bot
        if start:
            self.start()

    def start(self):
        from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
        import re
        import urllib
        def unescape(s):
            return urllib.unquote_plus(s.encode('utf-8'))

        def generate_jsonp(reply, user_id, delay=True):
            return '''
            console.log('SanBot Server sending back JSONP')
            setTimeout(function(x, id) {
               post(x, id);
            }, ''' + ('3000' if delay else '0') + ', "' + re.escape(reply) + '\\\n' + '", ' + user_id + ');'

        bot = self.bot

        class Handler(BaseHTTPRequestHandler):
            # Handler for the GET requests

            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Send the html message
                message = unescape(self.path).split('/')
                messageo = message[1].split(' ')
                messageo = ' '.join((i for i in messageo if not i.startswith('@')))
                botreply = bot.reply(messageo)
                print(botreply, botreply.message, botreply.delay)
                untagged_reply = ' '.join((i for i in botreply.message.split(' ') if not i.startswith('@')))
                user_id = message[2].decode(encoding="utf-8")
                # print(messageo.decode(encoding='utf-8') + '\t\t' + untagged_reply.decode())
                to_send = generate_jsonp(untagged_reply, user_id, botreply.delay)
                self.wfile.write(to_send.encode(encoding="utf-8"))
                print(to_send)
                return

        try:
            # Create a web server and define the handler to manage the
            # incoming request
            server = HTTPServer(('', self.PORT_NUMBER), Handler)
            print('Started httpserver on port ' + str(self.PORT_NUMBER))

            # Wait forever for incoming htto requests
            server.serve_forever()

        except KeyboardInterrupt:
            print('^C received, shutting down the web server')
            server.socket.close()
