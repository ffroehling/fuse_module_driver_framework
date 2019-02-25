import os
import config
import modules
import time
import sys
import logging
from fs import Filesystem
import subprocess

PID="/tmp/ab.pid"
var=3
runtime_modules = []

#This function loads all the modules and returns an array with every module
def load_modules():
    for m in modules.imports:
        #module = Module(m.module)
        #runtime_modules.append(module)
        #module.init()
        #m.module.init()
        runtime_modules.append(m.module)


def start(fs):
    #First check if folder exists -> if not create
    if not os.path.exists(config.BASEPATH):
        os.makedirs(config.BASEPATH)

    load_modules()
    fs = Filesystem(config.BASEPATH)
    #TODO: Add all modules
    #fs.add_module(runtime_modules[0])
    fs.start()

def stop(fs):
    load_modules()

    fs = Filesystem(config.BASEPATH)
    #TODO: unload all modules
    runtime_modules[0].stop()
    fs.stop()


if __name__ == "__main__":
    fs = Filesystem("%s" % config.BASEPATH)
        
    if len(sys.argv) == 2:
        #check params
        if sys.argv[1] == "start":
            fs.start()
        elif sys.argv[1] == "stop":
            fs.stop()
