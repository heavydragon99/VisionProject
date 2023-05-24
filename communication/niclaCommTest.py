# Pin Control Example
#
# This example shows how to use the I/O pins in GPIO mode.
import pyb
from pyb import Pin
#from machine import Pin

# Connect a switch to pin 0 that will pull it low when the switch is closed.
# Pin 1 will then light up.
pin0 = Pin('GPIO1', Pin.IN, Pin.PULL_UP)
pin1 = Pin('GPIO2', Pin.OUT_PP, Pin.PULL_NONE)
fromZumo = Pin("PA10", Pin.IN)
toZumo = Pin("PA9", Pin.OUT_PP)


toZumo.value(0)

while(1):
    while(fromZumo.value() == 1):    #No request received yet
        continue

    pyb.delay(100)
    toZumo.value(1)                 #Startbit (laag)
    pyb.delay(50)
    toZumo.value(0)                 #LSB (hoog)
    pyb.delay(50)
    toZumo.value(1)                 #Bit 1 (laag)
    pyb.delay(50)
    toZumo.value(1)                 #Bit 2 (laag)
    pyb.delay(50)
    toZumo.value(1)                 #Bit 3 (laag)
    pyb.delay(50)
    toZumo.value(0)                 #Bit 4 (hoog)
    pyb.delay(50)
    toZumo.value(0)                 #Bit 5 (hoog)
    pyb.delay(50)
    toZumo.value(1)                 #Bit 6 (laag)
    pyb.delay(50)
    toZumo.value(1)                 #MSB (laag)
    pyb.delay(50)
    toZumo.value(0)                 #Stopbit (hoog)
    #break
