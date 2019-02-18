#!/usr/bin/env python

from __future__ import print_function, absolute_import, division

import logging

from collections import defaultdict
from errno import ENOENT
from errno import EPERM
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from pprint import pprint



if not hasattr(__builtins__, 'bytes'):
    bytes = str


class Memory(LoggingMixIn, Operations):

    def add_module(self, module):
        now = time()

        if module in self.modules:
            #TODO: Log here that the module already exists
            print("Module already loaded")
            return False

        #first add the folder
        #self.add_folder(module.CONFIG['FOLDER'])
        #self.add_file("asdf", 3)
        self.add_folder("test1")
        self.add_folder("test2")
        self.add_folder("test3")
        self.add_file("test1/a", 3)
        self.add_file("test2/a", 3)
        self.add_file("test2/b", 3)
        self.add_file("test3/a", 3)
        self.add_file("test3/b", 3)
        self.add_file("test3/c", 3)

        #now add all the files
        #for device in module.CONFIG['DEVICES']:
            #self.add_file("%s/%s" % (module.CONFIG['FOLDER'], device['name']), device['size'])

    def add_folder(self, name):
        now = time()
        self.files['/' + name ] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2)

    def add_file(self, name, size):
        now = time()
        self.files['/' + name] = dict(
            st_mode=(S_IFREG | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2,
            st_size=size)

    def __init__(self):
        self.files = {}
        self.modules = []
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()

        self.files['/'] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2)

    def chmod(self, path, mode):
        raise FuseOSError(EPERM)
#        self.files[path]['st_mode'] &= 0o770000
#        self.files[path]['st_mode'] |= mode
#        return 0
#
    def chown(self, path, uid, gid):
        raise FuseOSError(EPERM)
        #self.files[path]['st_uid'] = uid
        #self.files[path]['st_gid'] = gid

    def create(self, path, mode):
        raise FuseOSError(EPERM)

#        self.files[path] = dict(
#            st_mode=(S_IFREG | mode),
#            st_nlink=1,
#            st_size=0,
#            st_ctime=time(),
#            st_mtime=time(),
#            st_atime=time())
#
#        self.fd += 1
#        return self.fd
#
    def getattr(self, path, fh=None):
        print("Path in getattr: %s" % path)
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path]

    def getxattr(self, path, name, position=0):
        attrs = self.files[path].get('attrs', {})

        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR

    def listxattr(self, path):
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()

    def mkdir(self, path, mode):
        raise FuseOSError(EPERM)
#        self.files[path] = dict(
#            st_mode=(S_IFDIR | mode),
#            st_nlink=2,
#            st_size=0,
#            st_ctime=time(),
#            st_mtime=time(),
#            st_atime=time())
#
#        self.files['/']['st_nlink'] += 1
#
    def open(self, path, flags):
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
        #pdb.set_trace()
#        print(path)
#        print("read")
#        print(offset)
#        print(size)
#        with open("/tmp/bla", "w") as f:
#            f.write("Path: %s\n" % path)
#            f.write("Offset: %d\n" % offset)
#            f.write("Size: %d\n" % size)
#
        return b"asfasdasdfasdf"
        #return self.data[path][offset:offset + size]

    def readdir(self, path, fh):
        #TODO: Handle this here
        print("readdir")
        print(path)

        l = {}
        appended = []

        for f in self.files:
            #print(self.files[f])
            if path in f:
                x = f.replace(path,'', 1)

                if x.startswith('/'):
                    x = x[1:]

                x = x.split('/')[0]
                if len(x) > 0 and x not in appended:
                    l[x] = f
                    #result.append(dict(x = self.files[f]))
                    appended.append(x)

        return l
        

        #return ['.', '..'] + [x[1:] for x in self.files if x != '/']
        return ['.', '..'] + [x[1:] for x in self.files if x == path]

    def readlink(self, path):
        #TODO: Handle this here
        return self.data[path]

    def removexattr(self, path, name):
        attrs = self.files[path].get('attrs', {})

        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR

    def rename(self, old, new):
        raise FuseOSError(EPERM)
        #self.data[new] = self.data.pop(old)
        #self.files[new] = self.files.pop(old)

    def rmdir(self, path):
        raise FuseOSError(EPERM)
        # with multiple level support, need to raise ENOTEMPTY if contains any files
        #self.files.pop(path)
        #self.files['/']['st_nlink'] -= 1

    def setxattr(self, path, name, value, options, position=0):
        print("setxattr")
        raise FuseOSError(EPERM)
        # Ignore options
        #attrs = self.files[path].setdefault('attrs', {})
        #attrs[name] = value

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        raise FuseOSError(EPERM)
#        self.files[target] = dict(
#            st_mode=(S_IFLNK | 0o777),
#            st_nlink=1,
#            st_size=len(source))
#
#        self.data[target] = source
#
    def truncate(self, path, length, fh=None):
        # make sure extending the file fills in zero bytes
        self.data[path] = self.data[path][:length].ljust(
            length, '\x00'.encode('ascii'))
        self.files[path]['st_size'] = length

    def unlink(self, path):
        raise FuseOSError(EPERM)
        #self.data.pop(path)
        #self.files.pop(path)

    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime

    def write(self, path, data, offset, fh):
        print("written to file")
        self.data[path] = (
            # make sure the data gets inserted at the right offset
            self.data[path][:offset].ljust(offset, '\x00'.encode('ascii'))
            + data
            # and only overwrites the bytes that data is replacing
            + self.data[path][offset + len(data):])
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)

#variables


class Filesystem:
    def __init__(self, mount):
        self.mount = mount
        self.mem = Memory()
        self.fuse = None
        logging.basicConfig(level=logging.DEBUG)

    #starts mounting the file system in userspace
    def start(self):
        if not self.fuse == None:
            print("Fuse is already started") #or whatever log system
            return False

        self.fuse = FUSE(self.mem, self.mount, foreground=True, allow_other=True)


    #stops fuse
    def stop(self):
        if self.fuse == None:
            print("Fuse is not started") #or whatever log system
            return False

        del self.fuse

    #adds a module
    def add_module(self, module):
        self.mem.add_module(module)

#if __name__ == '__main__':
#    import argparse
#    parser = argparse.ArgumentParser()
#    parser.add_argument('mount')
#    args = parser.parse_args()
#
#    logging.basicConfig(level=logging.DEBUG)
#    mem = Memory()
#    mem.add_file("test")
#    fuse = FUSE(mem, args.mount, foreground=True, allow_other=True)
