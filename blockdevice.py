import os 
import config
import watcher

class BlockDevice:
    instances = 0

    def __init__(self, folder, device):
        self.name = device['name']
        self.typ = device['typ']
        self.folder = folder
        self.loop_driver = self.get_loop_driver()
        self.path = "%s/%s/%s" % (config.BASEPATH, self.folder, self.name)
        BlockDevice.instances = (BlockDevice.instances + 1)

    def get_loop_driver(self):
        #make this a good call
        return 7

    def create(self):
        command = "mknod -m 777 %s %s %d %d" % (self.path, self.typ, self.loop_driver, BlockDevice.instances)
        print(command)
        os.system(command)

    def close(self):
        command = "unlink %s/%s/%s" % (config.BASEPATH, self.folder, self.name)
        print(command)
        os.system(command)

    def on_read(self):
        print("Read happened on %s" % self.name)
        os.system("echo asdf > /dev/relay/relay1")

    def on_write(self):
        print("Write happened on %s" % self.name)

    def add_read_watch(self):
        self.watch = watcher.add_read_listener(self.path, self.on_read)
        pass

    def add_write_watch(self):
        self.watch = watcher.add_write_listener(self.path, self.on_write)
        pass

    def add_read_write_watch(self):
        self.watch = watcher.add_read_write_listener(self.path, self.on_read, self.on_write)
        pass
