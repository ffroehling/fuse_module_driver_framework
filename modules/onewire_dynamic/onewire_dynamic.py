import os
###SECTION COMPONENT_MODEL
#The header section consists of the component model for the runtime enviroment
#Each module has to have this in the section

#CONFIG holds basic information
CONFIG = {
    #Name to be displayed
    "NAME" : 'ONEWIRE_DYNAMIC_TEMPERATURE_SENSOR',
    "FOLDER" : "onewire_dynamic",

    #These files will get allocated upon initalization
    #you can insert anything you want in attrs attribute
    #it will be given to on_read or on_write function
    "DEVICES" : [
        #{'name' : 'temp1', 'size' : 6, 'attrs' : {'path' : '/sys/bus/w1/devices/28-000005565c01'} }
    ]
}

#nothing special to init
def init():
    #build tempeature sensors here
    path = '/sys/bus/w1/devices/'
    
    counter = 1
    for (dirpath, dirnames, filenames) in os.walk(path):
        for item in dirnames:
            if not item.startswith("00-") and not item.startswith("w1_"):
            #found valid item
                CONFIG['DEVICES'].append({'name' : 'temp%d' % counter, 'size' : 6, 'attrs' : {'path' : '/sys/bus/w1/devices/%s' % item}})
                counter = counter + 1
    #print(dirnames)

#This function is for starting the logic
def on_read(device, size, offset):
    attrs = device[1]
    path = attrs['path']

    #read data
    with open('%s/w1_slave' % path, 'r') as f:
        raw = f.read()

        if not 'YES' in raw:
            #Error occured here. What todo?
            return None

        #get number of string
        temperature = int(raw[-6:])

        #set comma
        temperature = temperature / 1000

        #make it a float binary string
        r = ("{:.2f}".format(temperature)).encode('utf-8')

        #return it
        return r

#writes are not allowed
def on_write(device, value):
    return None

#nothing todo here
def stop():
    CONFIG['DEVICES'] = [] #reset to default
