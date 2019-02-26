import spidev

###SECTION COMPONENT_MODEL
#The header section consists of the component model for the runtime enviroment
#Each module has to have this in the section

#CONFIG holds basic information
CONFIG = {
    #Name to be displayed
    "NAME" : 'DIGITAL_ANALOG_CONVERTER',
    "FOLDER" : "dac",

    #These files will get allocated upon initalization
    #you can insert anything you want in attrs attribute
    #it will be given to on_read or on_write function
    "DEVICES" : [
        {'name' : 'dac1', 'size' : 3, 'attrs' : {'selection' : 0b0, 'last' : b'0\n'} },
        {'name' : 'dac2', 'size' : 3, 'attrs' : {'selection' : 0b1, 'last' : b'0\n'} }
    ]
}

#init everything -> set everything to zero
def init():
    for d in CONFIG['DEVICES']:
        on_write((d['name'], d['attrs']), b'0')

#This function is for starting the logic
def on_read(device, size, offset):
    attrs = device[1]
    last = attrs['last']

    return last


#Here the dac get's updated
def on_write(device, value):
    #prepare spi device
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 20000000 #Max frequency is 20MHz
    spi.mode = 0b00 #default mode. 0b11 is also supported, but not needed here

    perc = 0

    #convert parameter to int
    try:
        perc = int(value)
    except ValueError:
        return None
   
    #Values lower 0 and greater 100 are not allowed
    if perc < 0 or perc > 100: 
        return None

    #get bits of percentage
    #perc = perc_to_bits(perc)

    attrs = device[1]

    #config bits
    sel = attrs['selection']
    dc = 0
    ga = 1
    shdn = 1

    #set config bits
    config = (sel * (2**15)) + (dc * (2**14)) + (ga * (2**13)) + (shdn * (2**12))
    #config = sel + dc + ga + shdn

    #percentage mapping to 1024 scale ( 10 bit )
    perc = int(((1023 / 100) * perc))

    #perc is two byte, we need 10 bit -> left shift
    perc = perc << 2

    #combine config and percentage to 16 bit data string (whereas the two least significant bits are ignored by the chip)
    data = config + perc

    #convert to bytes
    to_write = list(data.to_bytes(2, byteorder='big'))

    #write to chip
    spi.xfer2(to_write)

    #close spi
    spi.close()

    #set last element
    attrs['last'] = value

    #return size of data
    return len(value)

#shutdown on close
def stop():
    for d in CONFIG['DEVICES']:
        on_write((d['name'], d['attrs']), b'0')

###END SECTION COMPONENT_MODEL
