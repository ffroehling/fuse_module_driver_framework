from . import relay
from . import dac
from . import onewire
from . import dht
from . import oled
#

#These are the modules which are started automaticly upon starting the abstraction
start = [
    onewire,
    dht
]

#Each module needs to be registered here
all_modules =  [
    relay,
    dac,
    onewire,
    dht,
    oled
]
