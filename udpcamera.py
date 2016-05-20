import subprocess, threading
import os

class camera:
    port=4444
    outfile='cam.jpg'
    timeout=5

    def __init__(s):
        try:
            os.remove(s.outfile)
        except:
            pass 

    def get_oneshot(s):
        def run():
            print "Thread started"
            s.proc = subprocess.Popen("gst-launch-0.10 udpsrc num-buffers=1 port=%s caps=\"image/jpeg, width=(int)1280, heigth=(int)720, framerate=30/1\" ! filesink location=%s" % (s.port, s.outfile), shell=True)
        
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
