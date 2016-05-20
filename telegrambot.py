import requests
import json
import tempfile
import os
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import cgi
from chat import chat


class PostHandlerCls(BaseHTTPRequestHandler):

    bot = ''

    def do_GET(self):
        s.send_response(200)
        s.end_headers()
        s.wfile.write('OK')

    def do_POST(self):

        #chat = chat(s.bot)

        #msg = ret['message']

        #ret = c.process(msg)

        #if ret:
        #   b.send_answer(ret[0], ret[1])

        self.send_response(200)
        self.end_headers()

        print "Income form: "

        print self.headers
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        length = int(self.headers['content-length'])

        if ctype == 'application/json':
            postvars = json.loads(self.rfile.read(length))
            c = chat(self.bot)
            msg = postvars['message']
            ret = c.process(msg)
             
            if ret:
                self.bot.send_answer(ret[0], ret[1])

        print postvars

        return

    def setbot(s, bot):
        s.bot = bot

class httpserver:
    def __init__(s, addr, port, token, ssl_public_cert, webhook_url):

        b = bot(token)

        if b.setWebhook(webhook_url, ssl_public_cert):

            print "Web hook was set"

            PostHandler = PostHandlerCls
            PostHandler.bot = b 

            server = HTTPServer((addr, port), PostHandler)

            print 'Starting server, use <Ctrl-C> to stop'
            server.serve_forever()

class bot:
    btoken = ""
    url = 'https://api.telegram.org'
    lastupdate = 0
    lastupdatepath = 'lastupdate'

    def __init__(self, token):
        self.btoken = token
	self.lastupdate = self.get_last_update()
	# print "Last update:", self.lastupdate

    def setWebhook(self, url, cert):
        postdata = {'url': url}
        files = {'certificate': ('bot-public.key', open(cert, 'rb'), 'application/data', {'Expires': '0'})}
       # print postdata
        r = requests.post(self.url + '/bot' + self.btoken + '/setWebhook', data = postdata, files = files )

        if r.json()['result'] == True:
            return True
        else:
            print r.json()
            return False 

    def get_last_update(self):
	f = open(self.lastupdatepath, 'r')
	update_id = f.readline().rstrip()
	f.close()
	if update_id:
	    return int(update_id)
    	else:
	    return 0

    def store_last_update(self, update_id):
	if update_id:
            self.lastupdate = update_id 
	    f = open(self.lastupdatepath, 'w')
	    f.write(str(update_id))
	    f.close()
	    return True
    	else:
	    return False

    def send_data(self, api_cmd, postdata = "", getdata = ""):
	if postdata:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	    r = requests.post(self.url + '/bot' + self.btoken + api_cmd, data = json.dumps(postdata), headers = headers)
	elif getdata:
	    r = requests.get(self.url + '/bot' + self.btoken + api_cmd + getdata)
	
	#print "Postata: ", postdata
	#print "Getdata: ", getdata
	if r.status_code == 200:
	    r.encoding = 'utf8'
	    
        return r.json() 

    def sendPhoto(self, username, filename):
        postdata = {'chat_id': username}
        files = {'photo': open(filename, 'rb')}

        r = requests.post(self.url + '/bot' + self.btoken + '/sendPhoto', data = postdata, files = files )

        #print postdata
        #print r.text
        if r.json()['result'] == True:
            return True
        else:
            print r.json()
            return False
        

    def getMe(self):
	return self.send_data('/getMe')

    def getFile(self, fid):
        postdata = {'file_id': fid}
        j = self.send_data('/getFile', postdata = postdata)
        
        if j['ok'] == True:
            r = requests.get(self.url + '/file/bot' + self.btoken + '/' + j['result']['file_path']) 

            (fd, fpath) = tempfile.mkstemp()
            f = os.fdopen(fd, 'w')
            f.write(r.content)
            f.close()

            return fpath
        else:
            return False
        

    def getUpdates(self, limit=10):
	getdata = "?offset=" + str(self.lastupdate + 1)
	json_ret = self.send_data('/getUpdates', getdata = getdata )

   	return json_ret 
    
    def send_answer(self, userid, msg):
        postdata = {'chat_id': userid, 'text': msg}
        json_ret = self.send_data('/sendMessage', postdata = postdata)
    
        return json_ret

    def get_next_message(self): 
	json_ret = self.getUpdates()

        if 'result' in json_ret:
	    for message in json_ret['result']:
	        self.store_last_update(message['update_id'])
	        yield message
        else:
            print "get_next_message Error"
            print json_ret 

