###SECTION COMPONENT_MODEL
#The header section consists of the component model for the runtime enviroment
#Each module has to have this in the section

#CONFIG holds basic information
CONFIG = {
    #Name to be displayed
    "NAME" : 'ONEWIRE_TEMPERATURE_SENSOR',
    "FOLDER" : "onewire",

    #These files will get allocated upon initalization
    #you can insert anything you want in attrs attribute
    #it will be given to on_read or on_write function
    "DEVICES" : [
        {'name' : 'temp1', 'size' : 6, 'attrs' : {'path' : '/sys/bus/w1/devices/28-000005565c01'} }
    ]
}

#nothing special to init
def init():
    pass

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
        temperature = int(data[-6:])

        #set comma
        temperature = temperature / 1000

        #make it a float binary string
        r = ("{:.2f}".format(b)).encode('utf-8')

        #return it
        return r

#writes are not allowed
def on_write(device, value):
    return None

#nothing todo here
def stop():
