This is a module which provides two files for controlling the MCP4812 chip. This is a digital to analog converter controlled via SPI.

Requirements:
This module needs a spidev interface from the kernel and obviously a connected MCP4812 chip to the spi port.  

Usage:
Write a percentage (0-100) value to the device file. The DAC will output the voltage according to its reference voltage (2,048V = 100%)
Any read returns the last written value.

