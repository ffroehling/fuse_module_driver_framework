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
    for m in modules.start:
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

                #When kill received -> quit
                if 'kill' in rec:
                    active = False
                    break
                
                result = self.action(rec)
                
                if not result is None:
                    self.response(result)
        #stop filesystem
        self.fs.stop()

        #reply
        self.response("Abstraction layer stopped")

        time.sleep(2)

        #cleanup
        os.remove(config.fifo_in_file)
        os.remove(config.fifo_out_file)
        os.remove('/tmp/abstractionstate')


    def unload_module(self, name):
        (succ, module) = self.fs.unload_module(name)

        if succ:
            #kill routine
            module.stop()
            return "Module successfully unloaded"

        return "No module with name %s loaded" % name

    def load_module(self, name):
        for module in modules.all_modules:
            m = module.module
            if m.CONFIG['NAME'] == name:
                #init module 
                m.init()

                #add to filesystem
                if self.fs.add_module(m):
                    return "Module successfully loaded"
                else:
                    return "Could not load module %s" % name

        return "Could not find module %s in module definition" % name

    def status(self):
        modules = self.fs.get_loaded_modules()

        response = "Currently loaded modules:\n"
        for m in modules:
            response += "\t- %s\n" % m.CONFIG['NAME']

        return response

    def action(self, rec):
        params = rec.split(" ")
        action = params[0]
        
        #first check single action params
        if action == "status":
            return self.status()
        
        #filter false params
        if not len(params) == 2:
            return "Invalid number of params received: %d (%s)" % (len(params), rec)

        param = params[1]

        if action == "unload":
            return self.unload_module(param)
        elif action == "load":
            return self.load_module(param)

        return "received: %s" % action

def start_fs(fs):
    #create a file for indicating running service
    with open('/tmp/abstractionstate', 'w') as f:
        f.write('running')

    modules = load_modules()
    for module in modules:
        #init module
        module.init()

        #add to file system
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
    if len(sys.argv) >= 2:
        #remove unneccessary item
        sys.argv.pop(0)

        #check params
        if sys.argv[0] == "start":
            nstart()
        elif sys.argv[0] == "stop":
            with open('/tmp/abstractionfifo_in', 'w') as f:
                f.write('kill\n')

            with open('/tmp/abstractionfifo_out', 'r') as f2:
                print(f2.read())
        elif sys.argv[0] == "status":
            if os.path.isfile('/tmp/abstractionstate'): 
                print("State: Running\n")

                with open('/tmp/abstractionfifo_in', 'w') as f:
                    f.write('status')

                with open('/tmp/abstractionfifo_out', 'r') as f2:
                    print(f2.read())
            else:
                print("State: Not running\n")
        else:
            p = " ".join([param for param in sys.argv]).replace('\n', '')

            with open('/tmp/abstractionfifo_in', 'w') as f:
                f.write('%s' % p)

            with open('/tmp/abstractionfifo_out', 'r') as f2:
                print(f2.read())

    else:
        print("TODO: print help here\n")
