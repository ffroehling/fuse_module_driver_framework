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
        {'name' : 'relay1', 'size' : 1, 'attrs' : dict()},
        {'name' : 'relay2', 'size' : 1, 'attrs' : dict()}
#        {'name' : 'relay3', 'typ' : 'c'},
#        {'name' : 'relay4', 'typ' : 'c'},
#        {'name' : 'relay5', 'typ' : 'c'}
    ]
}

#This function is called before initalization from the runtime environment
def pre_initialize():
    pass
    print("Module will be initialized")

#This function will be called immediatly after the initalization. It gets the devices parameter
def post_initialize(devices):
    print("Module has been initialized")
    devices[0].add_read_watch()

#This function is for starting the logic
def on_read(device, value):
    print("Module started")

def on_write(device, value):
    print("Module started")

#This function will be called right before runtime stops the module. Clean up your resources here
def pre_stop():
    print("Module will be stopped")
    pass

#After stopping you can do sth, e.g. logging
def post_stop():
    print("Module has been stopped")

###END SECTION COMPONENT_MODEL


###Logic can come here or somewhere else
###...


