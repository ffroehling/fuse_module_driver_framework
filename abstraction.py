import os
import config
import modules
import threading
import time

class BlockDevice:
    instances = 0

    def __init__(self, folder, device):
        self.name = device['name']
        self.typ = device['typ']
        self.folder = folder
        self.loop_driver = self.get_loop_driver()
        BlockDevice.instances = (BlockDevice.instances + 1)

    def get_loop_driver(self):
        #make this a good call
        return 7

    def create(self):
        command = "mknod %s/%s/%s %s %d %d" % (config.BASEPATH, self.folder, self.name, self.typ, self.loop_driver, BlockDevice.instances)
        print(command)
        os.system(command)

    def close(self):
        command = "unlink %s/%s/%s" % (config.BASEPATH, self.folder, self.name)
        print(command)
        os.system(command)

class Module():
    def __init__(self, instance):
        self.name = instance.CONFIG['NAME']
        self.devices = instance.CONFIG['DEVICES']
        self.folder = instance.CONFIG['FOLDER']
        self.pre_initialize = instance.pre_initialize
        self.post_initialize = instance.post_initialize
        self.post_stop = instance.post_stop
        self.on_read = instance.on_read
        self.on_write = instance.on_write

    def allocate_devices(self):
        self.allocated_devices = []

        for device in self.devices:
            d = BlockDevice(folder = self.folder, device = device)
            d.create()
            self.allocated_devices.append(d)

    def free_devices(self):
        for d in self.allocated_devices:
            d.close()

    def get_name(self):
        return self.name

    def init(self):
        self.pre_initialize()
        self.blockdevices = self.allocate_devices() 
        self.post_initialize(self.blockdevices)

    #start listening to the devices
    def start(self):
        #We need to do this in a new thread, but for now just call it
        self.start()

#This function loads all the modules and returns an array with every module
def load_modules():
    for m in modules.imports:
        module = Module(m.module)
        print(module)
        module.allocate_devices()
        time.sleep(5)
        module.free_devices()

load_modules()


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

