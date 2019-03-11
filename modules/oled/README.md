This is a module for controlling a small i2c display. It provides the ability to writeout 4 lines.

Requirements:
Enabled i2c interface, a small display (128x64 px, e.g. ssd1306) and the python luma package (https://github.com/rm-hull/luma.oled)

Usage:
The module provides four devices. Each of them belongs to a row on the screen. Just write your text to the device and it will appear on the screen.
