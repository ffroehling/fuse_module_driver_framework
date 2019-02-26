from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
import ImageFont

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
        {'name' : 'oled', 'size' : 3, 'attrs' : None },
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

    with canvas(device) as draw:
        #draw.rectangle(device.bounding_box, outline="white", fill="black")
        font = ImageFont.truetype("arial.ttf", 1)
        draw.text((30, 40), value.decode(), fill="white", font=font)

    return len(value)

#shutdown on close
def stop():
    global serial
    global device

    device.cleanup()
    serial.close()

###END SECTION COMPONENT_MODEL
