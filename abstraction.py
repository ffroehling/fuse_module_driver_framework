import os
import config
import modules
import time
from fs import Filesystem

runtime_modules = []

#This function loads all the modules and returns an array with every module
def load_modules():
    for m in modules.imports:
        #module = Module(m.module)
        #runtime_modules.append(module)
        #module.init()
        m.init()
        runtime_modules.append(m.module)

#first load the modules
load_modules()

#Create the virtual filesystem 
fs = Filesystem("%s" % config.BASEPATH)
fs.add_module(runtime_modules[0])
fs.start()
