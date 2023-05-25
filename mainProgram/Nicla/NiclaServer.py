import sensor, image, time, network, socket, sys, pyb
from pyb import Pin


#wifi Variable
SSID='NoName'           # Network SSID
KEY='Ab123456'          # Network key
HOST =''                # Use first available interface
PORT = 8080             # Arbitrary non-privileged port
imgCompression = 80     # Jpeg image compression

#uart Variable
pin0 = Pin('GPIO1', Pin.IN, Pin.PULL_UP)
pin1 = Pin('GPIO2', Pin.OUT_PP, Pin.PULL_NONE)
fromZumo = Pin("PA10", Pin.IN)
toZumo = Pin("PA9", Pin.OUT_PP)
toZumo.value(0)
uartDelayBegin = 20     # Delay before sending Uart
uartDelay = 10          # Delay between uart bits (plural of 2)

#Uart function no return value
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


#wifi function no return value
def sendImageRecieveCommand():
    # Init sensor
    sensor.reset()
    sensor.set_framesize(sensor.HVGA)
    sensor.set_pixformat(sensor.GRAYSCALE)

    # Init wlan module and connect to network
    print("Trying to connect... (This may take a while)...")
    wlan = network.WLAN(network.STA_IF)
    wlan.deinit()
    wlan.active(True)
    wlan.connect(SSID, KEY, timeout=20000)
    # We should have a valid IP now via DHCP
    print("WiFi Connected ", wlan.ifconfig())

    # Create server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    print("listen")
    # Bind and listen
    s.bind([HOST, PORT])
    s.listen(5)

    print("block")
    # Set server socket to blocking
    s.setblocking(True)
    clock = time.clock()
    while True:
        # Accept a client socket
        clientsock, addr = s.accept()
        print("Accepted connection from ", addr)
        response = clientsock.recv(16)
        print(response)
        clientsock.send(b'ready')
        while True:
            try:
                clock.tick()
                while(response != b'next'):
                    response = clientsock.recv(16)
                print("next")
                # Capture image
                img = sensor.snapshot()
                # Compress image to JPEG
                img_buf = img.compress(quality=imgCompression)

                clientsock.send(str(img_buf.size()))
                #print("img_buf.size")
                response = clientsock.recv(16)
                if(response == b'sizeok'):
                    #print("sizeok")
                    # Send image data to client
                    clientsock.sendall(img_buf)
                    response = clientsock.recv(16)
                    print("response" + str(response))

                    #todo intersection handeling
                    if(response == b"left"):
                        uartSendData(1)
                        pyb.delay(100)
                        uartSendData(1)
                        pyb.delay(100)
                        uartSendData(1)
                        pyb.delay(100)
                        uartSendData(1)
                        pyb.delay(100)
                        uartSendData(4)
                        pyb.delay(100)
                        uartSendData(4)
                        pyb.delay(100)
                        uartSendData(0)
                        pyb.delay(100)
                        while(1):
                            continue
                    else:
                        uartSendData(int(response))
                else:
                    print("Error: ", e)
                    # Close client socket
                    clientsock.close()
                    time.sleep(1)
                    break
                print(clock.fps())
            except Exception as e:
                print("Error: ", e)
                # Close client socket
                clientsock.close()
                time.sleep(1)
                break

#main Program
while(1):
    sendImageRecieveCommand()

