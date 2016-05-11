import os
from datetime import datetime
from dstemp import dstemp
import telegrambot as bot
import shutil

class chat:

    rootdir = '/data/aramilbot/files'
    fileurl = 'http://files.uranstation.ru'

    def __init__(s, bot):
        s.path = os.path.dirname(os.path.abspath(__file__)) + '/chat.txt'
        s.bot = bot
        s.d = dstemp()

    def save_chat(s, json):

        d = datetime.now()
        ddate = d.strftime("%Y%m%d %H:%M")
        print "Save chat"
        print json
        f = open(s.path, 'a')
        f.write(ddate + "\t" + json['from']['username'] + "\t" + json['text'] + "\n")
        f.close()

    def process(s, json):
        if json['chat']:
            username = json['chat']['username']
            chatid = json['chat']['id']

            if 'txt' in json: 
                txt = json['text']

                s.save_chat(json)

                if txt == '/temp':
                    return (chatid, s.d.dstemp_get())        
            
            if 'photo' in json:
                p = json['photo'][len(json['photo'])-1]
                w = p['width']
                h = p['height']
                fid = p['file_id']
                fsize = p['file_size']

                fpath = s.bot.getFile(fid)

                if fpath:
                    newname = s.rootdir + '/' + fid + '.jpg'
                    shutil.move(fpath, newname)
                    os.chmod(newname, 0644)

                    return (chatid, s.fileurl + '/' + os.path.basename(newname)) 
                else:
                    return (chatid, 'Can not download a file')
                    
    
