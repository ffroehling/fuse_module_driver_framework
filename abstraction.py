import os
import config
import modules
import time
import sys
import logging
from fs import Filesystem
import subprocess

runtime_modules = []

#This function loads all the modules and returns an array with every module
def load_modules():
    for m in modules.imports:
        runtime_modules.append(m.module)


def start(fs):
    #First check if folder exists -> if not create
    if not os.path.exists(config.BASEPATH):
        os.makedirs(config.BASEPATH)

    load_modules()

    for m in runtime_modules:
        try:
            m.init()
            fs.add_module(m)
        except Exception as e:
            #TODO: log exceptoin
            pass

    #finally start filesystem
    fs.start()

def stop(fs):
    load_modules()

    fs = Filesystem(config.BASEPATH)

    for m in runtime_modules:
        try:
            m.stop()
        except Exception as e:
            #TODO: log exceptoin
            pass

    fs.stop()

if __name__ == "__main__":
    fs = Filesystem("%s" % config.BASEPATH)
        
    if len(sys.argv) == 2:
        #check params
        if sys.argv[1] == "start":
            start(fs)
        elif sys.argv[1] == "stop":
            stop(fs)
