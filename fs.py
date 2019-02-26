#!/usr/bin/env python

from __future__ import print_function, absolute_import, division

import logging

from collections import defaultdict
from errno import ENOENT
from errno import EINVAL
from errno import EPERM
from errno import ENXIO
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn, fuse_exit
import subprocess

if not hasattr(__builtins__, 'bytes'):
    bytes = str

class Abstraction(LoggingMixIn, Operations):

    def add_module(self, module):
        now = time()

        if module in self.modules:
            #TODO: Log here that the module already exists
            return False

        #first add the folder
        self.add_folder(module.CONFIG['FOLDER'])

        #now add all the files
        for device in module.CONFIG['DEVICES']:
            self.add_file("%s/%s" % (module.CONFIG['FOLDER'], device['name']), device['size'])

        #Add to our list
        self.modules.append(module)

    #Adds a folder in the virtual file system
    def add_folder(self, name):
        now = time()
        self.files['/' + name ] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2)

    #Adds a file in the virtual file system
    def add_file(self, name, size):
        now = time()
        self.files['/' + name] = dict(
            st_mode=(S_IFREG | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_nlink=2,
            st_size=size)

    def get_module_for_path(self, path):
        if path == None:
            return None

        try:
            #get specific module 
            module = path.split('/')[1]
            
            for m in self.modules:
                if m.CONFIG['FOLDER'] == module:
                    return m

            return None

        except Exception as e:
            return None

    def get_device_for_path(self, module, path):
        if path == None or module == None:
            return (None, None)

        try:
            #get specific module 
            device = path.split('/')[2]

            for d in module.CONFIG['DEVICES']:
                if device == d['name']:
                    return (d['name'], d['attrs'])
            
            return (None, None)
        except Exception as e:
            return (None, None)

    def get_dm_for_path(self, path):
        module = self.get_module_for_path(path)
        device = self.get_device_for_path(module, path)

        return (module, device)

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

    def getattr(self, path, fh=None):
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

    def open(self, path, flags):
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
        #get module
        module, device = self.get_dm_for_path(path)
        
        #Raise error on any failure
        if module is None or device is None:
            raise FuseOSError(ENOENT)
            return b''

        result = module.on_read(device, size, offset)

        if result is None:
            raise FuseOSError(ENXIO)
            return b''

        return result

    def readdir(self, path, fh):
        l = {}
        appended = []

        for f in self.files:
            if path in f:
                x = f.replace(path,'', 1)

                if x.startswith('/'):
                    x = x[1:]

                x = x.split('/')[0]
                if len(x) > 0 and x not in appended:
                    l[x] = f
                    appended.append(x)

        return l

    def readlink(self, path):
        return self.data[path]

    def removexattr(self, path, name):
        attrs = self.files[path].get('attrs', {})

        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    #As no real write happens, no need todo anything
    def truncate(self, path, length, fh=None):
        pass

    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime

    def write(self, path, data, offset, fh):
        #get module
        module, device = self.get_dm_for_path(path)
        
        #Raise error on any failure
        if module is None or device is None:
            raise FuseOSError(ENOENT)
            return len(value)

        result = module.on_write(device, data)

        if result is None:
            raise FuseOSError(EINVAL)
            return len(data)

        return result

    #The following methods are not allowed in the filesystem
    def unlink(self, path):
        raise FuseOSError(EPERM)

    def chmod(self, path, mode):
        raise FuseOSError(EPERM)

    def chown(self, path, uid, gid):
        raise FuseOSError(EPERM)

    def create(self, path, mode):
        raise FuseOSError(EPERM)

    def symlink(self, target, source):
        raise FuseOSError(EPERM)

    def rmdir(self, path):
        raise FuseOSError(EPERM)

    def setxattr(self, path, name, value, options, position=0):
        raise FuseOSError(EPERM)

    def rename(self, old, new):
        raise FuseOSError(EPERM)

    def mkdir(self, path, mode):
        raise FuseOSError(EPERM)

class Filesystem:
    def __init__(self, mount):
        self.mount = mount
        self.mem = Abstraction()
        self.fuse = None
        #logging.basicConfig(level=logging.DEBUG)

    #starts mounting the file system in userspace
    def start(self):
        if not self.fuse == None:
            return False

        self.fuse = FUSE(self.mem, self.mount, foreground=False, allow_other=True)

    def stop(self):
        subprocess.run(['umount', self.mount ])


    #adds a module
    def add_module(self, module):
        self.mem.add_module(module)
