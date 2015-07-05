import requests

class bot:
    btoken = ""
    url = 'https://api.telegram.org/bot'

    def __init__(self, token):
        self.btoken = token

    def send_data(self, api_cmd, data = ""):
	r = requests.post(self.url + self.btoken + api_cmd, data = data)
	if r.status_code == 200:
	    return r.content
        return False 

    def getme(self):
	return self.send_data('/getMe')
    	
    
