import subprocess
from datetime import datetime

tpath = '/data/var/www/temp/temp'

def dstemp_get():
    d = datetime.datetime.now()
    dt = d.strftime("%Y%m%d")

    line = subprocess.check_output(['tail', '-1', "%s/dstemp-%s.csv" % (tpath, dt)])

    l = line.split(",")

    print l
    
    return "Time: %s, temperature: %s C" % (l[0].split(" ")[1], l[2].strip())
        

        
