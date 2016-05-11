import requests
import json
import tempfile
import os

class bot:
    btoken = ""
    url = 'https://api.telegram.org'
    lastupdate = 0
    lastupdatepath = 'lastupdate'

    def __init__(self, token):
        self.btoken = token
	self.lastupdate = self.get_last_update()
	print "Last update:", self.lastupdate

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
	
	print "Postata: ", postdata
	print "Getdata: ", getdata
	#r = requests.post(self.url + self.btoken + api_cmd, data = postdata)
	if r.status_code == 200:
	    r.encoding = 'utf8'
	    
        return r.json() 

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
	for message in json_ret['result']:
	    self.store_last_update(message['update_id'])
	    yield message

