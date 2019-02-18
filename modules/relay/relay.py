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
        {'name' : 'relay1', 'size' : 16, 'attrs' : dict()},
        {'name' : 'relay2', 'size' : 16, 'attrs' : dict()}
    ]
}

#This function is for starting the logic
def on_read(device, size, offset):
    print("Module read")
    print(device)
    #print(device[0])
    #print(device[1])

    return b'i have been read'

def on_write(device, value):
    print("written")
    print(value)

    return len(value)

###END SECTION COMPONENT_MODEL


###Logic can come here or somewhere else
###...


