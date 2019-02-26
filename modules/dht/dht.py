###SECTION COMPONENT_MODEL
#The header section consists of the component model for the runtime enviroment
#Each module has to have this in the section

#CONFIG holds basic information
CONFIG = {
    #Name to be displayed
    "NAME" : 'DHT_TEMPERATURE_SENSOR',
    "FOLDER" : "dht",

    #These files will get allocated upon initalization
    #you can insert anything you want in attrs attribute
    #it will be given to on_read or on_write function
    "DEVICES" : [
        {'name' : 'temp', 'size' : 6, 'attrs' : {'path' : '/sys/bus/iio/devices/iio:device1/in_temp_input'} },      
        {'name' : 'humidity', 'size' : 6, 'attrs' : {'path' : '/sys/bus/iio/devices/iio:device1/in_humidityrelative_input'} }  
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
    with open('path', 'r') as f:
        raw = f.read()

        #get number of string
        data = int(raw[-6:])

        #set comma
        data = data / 1000

        #make it a float binary string
        r = ("{:.2f}".format(data)).encode('utf-8')

        #return it
        return r

#writes are not allowed
def on_write(device, value):
    return None

#nothing todo here
def stop():
    pass
