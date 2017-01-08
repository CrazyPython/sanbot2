from response import Response
import time
import random

__all__ = ['limit', 'coinflip', 'punc_strip', 'Timer', 'input', 'front_strip', 'to_repsonse_obj']


def limit(n, limit):
    if n > limit:
        return limit
    else:
        return n


def coinflip():
    return random.choice((True, False))


def punc_strip(message):
    return ''.join(char for char in message.strip() if char not in '.?!-/*\\')


def front_strip(message, to_strip):
    if message.startswith(to_strip):
        return message[len(to_strip):]
    else:
        return message


def to_repsonse_obj(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            return Response(result)
        else:
            return result  # don't turn into response object on falsey value

    return inner


class Timer(object):
    def __init__(self):
        self.start_time = time.time()

    def get_time(self):
        return time.time() - self.start_time


try:
    raw_input
except NameError:
    pass
else:
    input = raw_input
