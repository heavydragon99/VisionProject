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

uartDelayBegin = 20;
uartDelay = 10;



def uartSendData(data):

    bits = []
    for i in range(8):
        bit = (data >> i) & 1
        bits.append(not bit)


    #print(bits);
    #print(bits[0]);
    while(fromZumo.value() == 1):    #No request received yet
        continue

    print("send data")
    pyb.delay(uartDelayBegin)
    toZumo.value(1)                 #Startbit (laag)
    pyb.delay(uartDelay)
    toZumo.value(bits[0])                 #LSB (hoog)
    pyb.delay(uartDelay)
    toZumo.value(bits[1])                 #Bit 1 (laag)
    pyb.delay(uartDelay)
    toZumo.value(bits[2])                 #Bit 2 (laag)
    pyb.delay(uartDelay)
    toZumo.value(bits[3])                 #Bit 3 (laag)
    pyb.delay(uartDelay)
    toZumo.value(bits[4])                 #Bit 4 (hoog)
    pyb.delay(uartDelay)
    toZumo.value(bits[5])                 #Bit 5 (hoog)
    pyb.delay(uartDelay)
    toZumo.value(bits[6])                 #Bit 6 (laag)
    pyb.delay(uartDelay)
    toZumo.value(bits[7])                 #MSB (laag)
    pyb.delay(uartDelay)
    toZumo.value(0)                 #Stopbit (hoog)



while(1):
    pyb.delay(100);
    uartSendData(3);

