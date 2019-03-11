import os
import config
import modules
import time
import sys
import time
import logging
from threading import Thread
from fs import Filesystem


#This function loads all the modules and returns an array with every module
def load_modules():
    runtime_modules = []
    for m in modules.imports:
        runtime_modules.append(m.module)

    return runtime_modules

class Listener():
    def __init__(self, fs):
        #TODO: Create fifos here
        try:
            self.fifo_in = os.mkfifo(config.fifo_in_file)
            self.fifo_out = os.mkfifo(config.fifo_out_file)
            self.fs = fs
        except OSError as e:
            print("Failed to create FIFO: %s" % str(e))

    def response(self, value):
        with open(config.fifo_out_file, 'w') as fo:
            fo.write(value)

    #reads the device and returns a value
    def listen(self):
        active = True
        while active:
            with open(config.fifo_in_file, 'r') as fi:
                #read data
                rec = fi.read()

                #When quit -> quit
                if 'kill' in rec:
                    active = False
                    break
                
                result = self.action(rec)
                
                if not result is None:
                    self.response(result)
        #stop filesystem
        self.fs.stop()

        #cleanup
        os.remove(config.fifo_in_file)
        os.remove(config.fifo_out_file)

    def action(self, action):
        return "received: %s" % action

def start_fs(fs):
    modules = load_modules()
    for module in modules:
        fs.add_module(module)

    fs.start()

def listener(fs):
    listener = Listener(fs)
    listener.listen()

def fork():
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit first parent
            sys.exit(0) 
    except OSError as e: 
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # decouple from parent environment
    os.setsid() 
    os.umask(0) 

    # do second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            # exit from second parent
            sys.exit(0) 
    except OSError as e: 
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1) 

def nstart():
    fork()

    fs = Filesystem("%s" % config.BASEPATH)

    #threads
    t_fs = Thread(target = start_fs, args=(fs,))
    t_listener = Thread(target = listener, args=(fs,))

    #start
    t_fs.start()
    t_listener.start()

    t_fs.join()
    t_listener.join()
    

if __name__ == "__main__":
    #fs = Filesystem("%s" % config.BASEPATH)
    if len(sys.argv) == 2:
        #runner = Runner()
        #check params
        if sys.argv[1] == "start":
            nstart()

        elif sys.argv[1] == "status":
            with open('/tmp/abstractionfifo_in', 'w') as f:
                f.write('status\n')

                with open('/tmp/abstractionfifo_out', 'r') as f2:
                    print(f2.read())

        elif sys.argv[1] == "stop":
            with open('/tmp/abstractionfifo_in', 'w') as f:
                f.write('kill\n')

                with open('/tmp/abstractionfifo_out', 'r') as f2:
                    print(f2.read())
