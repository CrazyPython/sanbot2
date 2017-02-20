#!/usr/bin/python
import sys
from interface import StackExchangeWeb
from main import SanBot

if len(sys.argv) > 1:
   corpus = sys.argv[1]
else:
   corpus = 'news2'

bot = SanBot(corpus=corpus)
StackExchangeWeb(bot)
