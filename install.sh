#!/usr/bin/env bash
go get github.com/pteichman/fate/cmd/fate-console
pip_pypy install twython nltk cobe chatexchange
chmod 755 console.py
cobe set-stemmer english
pypy train.py
cobe learn train.txt
mv cobe.brain $1