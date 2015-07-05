#!/usr/bin/env python

import telegrambot as bot

TOKENFILE = '/data/aramilbot/token'

f = open(TOKENFILE, 'r')
token = f.readline()
f.close()

if token:
    print token
    b = bot.bot(token.rstrip())

    print b.getme()	
