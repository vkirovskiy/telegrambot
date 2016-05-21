import subprocess, threading
import os

class camera:
    port=4444
    host=''
    outfile='cam.jpg'
    timeout=5

    def __init__(s, host, port):

        s.host = host
        s.port = port
        try:
            os.remove(s.outfile)
        except:
            pass 

    def get_oneshot(s):
        def run():
            print "Thread started"
            s.proc = subprocess.Popen("gst-launch-0.10 tcpclientsrc host=%s port=%s num-buffers=200 ! filesink location=%s" % (s.host, s.port, s.outfile), shell=True)
        
            print "Thread finished"

            s.proc.communicate()

        thread = threading.Thread(target=run)
        thread.start()
        thread.join(s.timeout)

        if thread.is_alive():
            s.proc.terminate()
            print "Thread terminated"
            thread.join()

        if os.path.isfile(s.outfile):
            r = s.proc.returncode
            if r == 0:
                return ("OK", s.outfile)
            elif r == -15:
                return ("Camera is offline",'')
            else:
                return ("Error " + str(r), '')
        else:
            return "Error"
