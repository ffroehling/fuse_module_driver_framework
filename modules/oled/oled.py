from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
from PIL import ImageFont, ImageDraw

###SECTION COMPONENT_MODEL
#The header section consists of the component model for the runtime enviroment
#Each module has to have this in the section

#CONFIG holds basic information
CONFIG = {
    #Name to be displayed
    "NAME" : 'OLED_DISPLAY',
    "FOLDER" : "oled",

    #These files will get allocated upon initalization
    #you can insert anything you want in attrs attribute
    #it will be given to on_read or on_write function
    "DEVICES" : [
        {'name' : 'row1', 'size' : 3, 'attrs' : {'height' : 10, 'value' : ''} },
        {'name' : 'row2', 'size' : 3, 'attrs' : {'height' : 20, 'value' : ''} },
        {'name' : 'row3', 'size' : 3, 'attrs' : {'height' : 30, 'value' : ''} },
        {'name' : 'row4', 'size' : 3, 'attrs' : {'height' : 40, 'value' : ''} },
    ]
}

#global vars
serial = None
device = None


#init everything -> set everything to zero
def init():
    global serial
    global device

    serial = i2c(port=0, address=0x3C)
    device = ssd1306(serial)

#Read not allowed yet
def on_read(device, size, offset):
    return None


#Here the dac get's updated
def on_write(d, value):
    global serial
    global device

    attrs = d[1]
    attrs['value'] = value.decode()

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")

        for dev in CONFIG['DEVICES']:
            v = dev['attrs']['value']
            h = dev['attrs']['height']

            draw.text((10, h), v, fill="white")

    return len(value)

#shutdown on close
def stop():
    global serial
    global device

    #device.cleanup()
    #serial.close()

###END SECTION COMPONENT_MODEL
