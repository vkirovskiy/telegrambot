#!/usr/bin/env python

import sys
import time
import telegrambot as bot
from chat import chat

TOKENFILE = sys.argv[1] 

f = open(TOKENFILE, 'r')
token = f.readline()
f.close()


def debug(msg):
    print "Debug -- "
    print msg

if token:
    print token
    b = bot.bot(token.rstrip())
    c = chat(b)

    while True:
        print "Processing..."

        for ret in b.get_next_message():
            print ret

            msg = ret['message'] 
            
            ret = c.process(msg)
    
            if ret:
               b.send_answer(ret[0], ret[1]) 


        time.sleep(10)
            

