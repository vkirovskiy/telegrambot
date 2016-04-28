import subprocess
from datetime import datetime

class dstemp:

    def __init__(s):
        s.path = '/data/var/www/temp/temp'

    def dstemp_get(s):
        d = datetime.now()
        dt = d.strftime("%Y%m%d")

        line = subprocess.check_output(['tail', '-1', "%s/dstemp-%s.csv" % (s.path, dt)])

        l = line.split(",")

        return "Time: %s, temperature: %s C" % (l[0].split(" ")[1], l[2].strip())
        

        
