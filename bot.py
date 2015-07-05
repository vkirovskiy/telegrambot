#!/usr/bin/env python

import sys
import telegrambot as bot

TOKENFILE = sys.argv[1] 

f = open(TOKENFILE, 'r')
token = f.readline()
f.close()

if token:
    print token
    b = bot.bot(token.rstrip())

    for ret in b.get_next_message():
	print ret 

