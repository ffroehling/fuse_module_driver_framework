import os
import config
import modules
import threading
import time
import watcher
from blockdevice import BlockDevice
from module import Module


runtime_modules = []

#This function loads all the modules and returns an array with every module
def load_modules():
    for m in modules.imports:
        module = Module(m.module)
        runtime_modules.append(module)
        module.init()

def stop_modules():
    for module in runtime_modules:
        module.stop()

        #time.sleep(5)
        #module.free_devices()


load_modules()
watcher.start_listening()

time.sleep(10)

watcher.stop_listening()
stop_modules()

#def i():
#    modules = []
#    for module in os.listdir(os.path.dirname('./modules/')):
#        if not module == '__init__.py' and module[-3:] != '.py':
#            __import__(module)
#            modules.append({config = module.CONFIG})
#        #    continue
#        #__import__(module[:-3], locals(), globals())
#            print(module)
#    #import modules
#
#device = BlockDevice(folder = "/tmp", name="test", 1)
#i()
##pprint(modules.relay)
#pprint(modules.relay)

#print(modules.imports)
    #module.start()
#print(dir(modules.relay))
