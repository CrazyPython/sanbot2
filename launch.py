#!/usr/bin/env python3
import getpass
import logging
import logging.handlers
import os
import random
import sys
import time
from main import SanBot
from response import Response

import chatexchange.client
import chatexchange.events
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("model", help="the model to use")
parser.add_argument("--passive",
                    help="learn in TNB instead, not responding to messages. Will learn using specified model",
                    action="store_true")
parser.add_argument("--secondary",
                    help="Run under the secondary account",
                    action="store_true")
args = parser.parse_args()

sanbot = SanBot(corpus=sys.argv[1])
botname = 'SanBot'

logger = logging.getLogger(__name__)

if args.secondary:
    botname = 'NamelessBot'

def main():
    setup_logging()

    # Run `. setp.sh` to set the below testing environment variables

    host_id = 'stackexchange.com'
    if not args.passive:
        room_id = '30332'
    else:
        room_id = '240'

    if 'ChatExchangeU' in os.environ:
        email = os.environ['ChatExchangeU']
    else:
        email = raw_input("Email: ")
    if 'ChatExchangeP' in os.environ:
        password = os.environ['ChatExchangeP']
    else:
        password = getpass.getpass("Password: ")

    client = chatexchange.client.Client(host_id)
    client.login(email, password)

    room = client.get_room(room_id)
    room.join()
    room.watch(on_message)

    print("(You are now in room #%s on %s.)" % (room_id, host_id))
    if not args.passive:
        room.send_message("{} restarted.".format(botname))
    while True:
        time.sleep(100)
    client.logout()


def on_message(message, client):
    if not isinstance(message, chatexchange.events.MessagePosted):
        # Ignore non-message_posted events.
        logger.debug("event: %r", message)
        return

    print(">> (%s) %s" % (message.user.name.encode('ascii', 'ignore'), message.content.encode('ascii', 'ignore')))
    if not args.passive:
        if not message.content.startswith('NOREPLY') and message.user.name != botname:
            print(message)
            print("Spawning thread")
            raw_message = sanbot.reply(message.content)
            try:
                reply = str(raw_message.message)  # ignores delay
            except:
                print(">> recovered from error")
            else:
                try:
                    message.message.reply(reply.encode('ascii', 'replace'))
                except UnicodeEncodeError:
                    print(">> recovered from unicode encode error")
    else:
        sanbot.brain.learn(message.content)
        print(">> learned message")


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.DEBUG)

    # In addition to the basic stderr logging configured globally
    # above, we'll use a log file for chatexchange.client.
    wrapper_logger = logging.getLogger('chatexchange.client')
    wrapper_handler = logging.handlers.TimedRotatingFileHandler(
        filename='client.log',
        when='midnight', delay=True, utc=True, backupCount=7,
    )
    wrapper_handler.setFormatter(logging.Formatter(
        "%(asctime)s: %(levelname)s: %(threadName)s: %(message)s"
    ))
    wrapper_logger.addHandler(wrapper_handler)


if __name__ == '__main__':
    main()
