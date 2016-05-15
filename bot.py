#!/usr/bin/env python

import sys
import time
import telegrambot as bot
from chat import chat

if len(sys.argv) < 4:
    print "Usage: python ./bot.py token_file ssl_public_cert webhook_url"
    sys.exit(1)

TOKENFILE = sys.argv[1] 
ssl_public_cert = sys.argv[2]
webhook_url = sys.argv[3]

f = open(TOKENFILE, 'r')
token = f.readline()
f.close()


def debug(msg):
    print "Debug -- "
    print msg

if token:
    print token
    s = bot.httpserver('127.0.0.1', 9090, token.rstrip(), ssl_public_cert, webhook_url)

