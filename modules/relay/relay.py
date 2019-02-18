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
        {'name' : 'relay1', 'size' : 1, 'attrs' : dict(gpio : '/sys/class/gpio/A23')},
        {'name' : 'relay1', 'size' : 1, 'attrs' : dict(gpio : '/sys/class/gpio/A24')},
    ]
}

#This function is for starting the logic
def on_read(device, size, offset):
    attr = device[1]
    with open(attr.gpio, 'rb') as f:
        data = f.read()
        return data

    return b'0'

def on_write(device, value):
    attr = device[1]
    with open(attr.gpio, 'wb') as f:
        f.write(value)
        return data

    return len(value)

###END SECTION COMPONENT_MODEL


###Logic can come here or somewhere else
###...


