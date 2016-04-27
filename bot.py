#!/usr/bin/env python

import sys
import time
import telegrambot as bot
from dstemp import dstemp_get
from chat import chat

TOKENFILE = sys.argv[1] 

f = open(TOKENFILE, 'r')
token = f.readline()
f.close()

if token:
    print token
    b = bot.bot(token.rstrip())
    c = chat()

    while True:
        print "Processing..."

        for ret in b.get_next_message():
            msg = ret['message'] 
            if msg['chat']:
                txt = msg['text']

                c.save_chat(msg)

                if txt == '/temp':
                    chatid = msg['chat']['id']
                    print b.send_answer(chatid, dstemp_get())

        time.sleep(10)
            

