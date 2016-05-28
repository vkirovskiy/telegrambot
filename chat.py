import os
from datetime import datetime
from dstemp import dstemp
import telegrambot as bot
import udpcamera as camera
import shutil

class chat:

    rootdir = '/data/aramilbot/files'
    fileurl = 'http://files.uranstation.ru'
    usbcamera = ('192.168.2.7', 4444)

    def __init__(s, bot):
        s.path = os.path.dirname(os.path.abspath(__file__)) + '/chat.txt'
        s.bot = bot
        s.d = dstemp()

    def save_chat(s, user, text):

        d = datetime.now()
        ddate = d.strftime("%Y%m%d %H:%M")
        print "Save chat"
        f = open(s.path, 'a')
        f.write(ddate + "\t" + user + "\t" + text + "\n")
        f.close()

    def process(s, json):
        if json['chat']:
            username = json['chat']['username']
            chatid = json['chat']['id']

            if 'text' in json: 
                txt = json['text']

                s.save_chat(username, txt)

                if txt == '/temp':
                    return (chatid, s.d.dstemp_get())        

                if txt == '/cam':
                    cam = camera.camera(s.usbcamera[0], s.usbcamera[1])
                    (st, f) = cam.get_oneshot()

                    if st == 0:
                        s.bot.sendPhoto(chatid, f)
                        return None 
                    elif st == -15:
                        return (chatid, 'Timeout to connect')
                    elif st == 255:
                        return (chatid, 'Camera is offline')

                    return (chatid, st)
            
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

                    s.save_chat(username, 'Picture ' + newname)
                    return (chatid, s.fileurl + '/' + os.path.basename(newname)) 
                else:
                    return (chatid, 'Can not download a file')
                    
    
