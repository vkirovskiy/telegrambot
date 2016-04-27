import os
from datetime import datetime

class chat:

    def __init__(s):
        s.path = os.path.dirname(os.path.abspath(__file__)) + '/chat.txt'

    def save_chat(s, json):

        d = datetime.now()
        ddate = d.strftime("%Y%m%d %H:%M")
        print "Save chat"
        print json
        f = open(s.path, 'a')
        f.write(ddate + "\t" + json['from']['username'] + "\t" + json['text'] + "\n")
        f.close()
    
