#!/usr/local/bin/pypy
from __future__ import print_function, division
from utils import *
import sys

timer = Timer()
print("SanBot is starting... ", end="")
sys.stdout.flush()
from main import SanBot

if '--no-debug' in sys.argv or '-nd' in sys.argv:
    debug = False
else:
    debug = True

sanbot = SanBot(debug=debug)
print("done. (took {:.1f} seconds.)".format(timer.get_time()))
while True:
    print(sanbot.reply(input('{:5.1f} > '.format(sanbot.feelings[1])))[0])
