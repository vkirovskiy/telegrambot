#!/usr/bin/env python

import sys
import time
import telegrambot as bot
from chat import chat
import argparse

parser = argparse.ArgumentParser(description='Telegram bot')
parser.add_argument('--tokenfile', help='Token file', required=True)
parser.add_argument('--sslcert', help='Public cert for telegram webhook', required=True)
parser.add_argument('--whookurl', help='Webhook url', required=True)

args = parser.parse_args()

TOKENFILE = args.tokenfile 
ssl_public_cert = args.sslcert
webhook_url = args.whookurl

f = open(TOKENFILE, 'r')
token = f.readline()
f.close()


def debug(msg):
    print "Debug -- "
    print msg

if token:
    print token
    s = bot.httpserver('127.0.0.1', 9090, token.rstrip(), ssl_public_cert, webhook_url)

