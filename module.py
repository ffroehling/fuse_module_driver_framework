from blockdevice import BlockDevice
import config

class Module():
    def __init__(self, instance):
        self.name = instance.CONFIG['NAME']
        self.devices = instance.CONFIG['DEVICES']
        self.folder = instance.CONFIG['FOLDER']
        self.pre_initialize = instance.pre_initialize
        self.post_initialize = instance.post_initialize
        self.pre_stop = instance.pre_stop
        self.post_stop = instance.post_stop
        self.on_read = instance.on_read
        self.on_write = instance.on_write

    def allocate_devices(self):
        self.allocated_devices = []

        for device in self.devices:
            #create a block device
            d = BlockDevice(folder = self.folder, device = device)
            d.create()

            #add it to array
            self.allocated_devices.append(d)

    def free_devices(self):
        for d in self.allocated_devices:
            d.close()

    def get_name(self):
        return self.name

    def init(self):
        self.pre_initialize()
        self.blockdevices = self.allocate_devices() 
        self.post_initialize(self.allocated_devices)

    def stop(self):
        self.pre_stop()
        self.free_devices()
        self.post_stop()
