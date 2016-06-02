from subprocess import Popen, PIPE, STDOUT
import threading
import os
import sys

class scripts:

    spath = '' 
    timeout = 10

    def __init__(s, spath):
        if spath:
            s.spath = spath   
        else:
            s.spath = os.path.dirname(os.path.realpath(sys.argv[0]))

    def execute(s, cmdline):
        def run():
            print "Thread started"
            
            if os.path.exists(s.spath + '/' + cmdline):
                s.proc = Popen(s.spath + '/' + cmdline, shell=True, stderr=STDOUT, stdout=PIPE)
            else:
                print "No such file"

            print "Thread finished"

            #s.proc.communicate()

        thread = threading.Thread(target=run)
        thread.start()
        thread.join(s.timeout)

        if hasattr(s, 'proc'):
            (sout, serr) = s.proc.communicate()

            if thread.is_alive():
                s.proc.terminate()
                print "Thread terminated"
                thread.join()        
            
            return (sout, serr)
        else:
            return (None, 'No such file')
