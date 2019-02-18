###SECTION COMPONENT_MODEL
#The header section consists of the component model for the runtime enviroment
#Each module has to have this in the section

#CONFIG holds basic information
CONFIG = {
    #Name to be displayed
    "NAME" : 'RELAY_CONTROL',
    "FOLDER" : "relay",

    #These files will get allocated upon initalization
    #you can insert anything you want in attrs attribute
    #it will be given to on_read or on_write function
    "DEVICES" : [
        {'name' : 'relay1', 'size' : 1, 'attrs' : { 'allocate' : 23, 'direction' : 'out', 'path' : '/sys/class/gpio/pioA23/'}},
        {'name' : 'relay2', 'size' : 1, 'attrs' : { 'allocate' : 24, 'direction' : 'out', 'path' : '/sys/class/gpio/pioA24/'}}
    ]
}

def init():
    for d in CONFIG['DEVICES']:
        attrs = d['attrs']

        #allocate gpio
        with open("/sys/class/gpio/export", "wb") as f:
            f.write(b"%d\n" % attrs['allocate'])

        #set direction
        with open("%s/direction" % attrs['path'], "wb") as f:
            f.write(b"%s\n" % attrs['direction'])

#This function is for starting the logic
def on_read(device, size, offset):
    attr = device[1]
    with open(attr['gpio'], 'rb') as f:
        data = f.read()
        return data

    return b'0'

def on_write(device, value):
    attr = device[1]
    with open(attr['gpio'], 'wb') as f:
        f.write(value)

    return len(value)

###END SECTION COMPONENT_MODEL


###Logic can come here or somewhere else
###...


