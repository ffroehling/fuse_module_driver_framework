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
        {'name' : 'relay1', 'size' : 1, 'attrs' : { 'gpio' : '/sys/class/gpio/pioA23/value'}},
        {'name' : 'relay2', 'size' : 1, 'attrs' : {'gpio' : '/sys/class/gpio/pioA24/value'}}
    ]
}

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


