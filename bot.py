#!/usr/bin/env python

import sys
import time
import telegrambot as bot
from chat import chat
import argparse

parser = argparse.ArgumentParser(description='Telegram bot')
parser.add_argument('--tokenfile', help='Token file', required=True)
parser.add_argument('--sslcert', help='Public cert for telegram webhook')
parser.add_argument('--whookurl', help='Webhook url')
parser.add_argument('-w', help='Use webhook', action='store_const', const=1)

args = parser.parse_args()

TOKENFILE = args.tokenfile 
ssl_public_cert = args.sslcert
webhook_url = args.whookurl

f = open(TOKENFILE, 'r')
token = f.readline().rstrip()
f.close()


def debug(msg):
    print "Debug -- "
    print msg

if token:
    print token
    
    tbot = bot.bot(token)

    if args.w and ssl_public_cert and webhook_url:
        print "Webhook mode enabled"
        tbot = bot.bot(token)
        s = bot.httpserver('127.0.0.1', 9090, tbot, ssl_public_cert, webhook_url)
    else:
        print "Webhook mode disabled"
        print "Reseting exists webhook... " + str(tbot.resetWebhook())
        
        from chat import chat

        c = chat(tbot)

        print "Processing... "

        while True:
            print '...'
            
            for ret in tbot.get_next_message():
                print ret

                msg = ret['message'] 
                ret = c.process(msg)
    
                if ret:
                    tbot.send_answer(ret[0], ret[1])
            
            time.sleep(10)
        
    

