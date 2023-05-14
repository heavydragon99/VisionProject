import sensor, image, time, network, socket, sys

SSID='NoName'      # Network SSID
KEY='Ab123456'       # Network key
HOST ='192.168.137.200'     # Use first available interface
PORT = 8080  # Arbitrary non-privileged port
imgCompression = 95 #jpeg image compression

# Init sensor
sensor.reset()
sensor.set_framesize(sensor.QVGA)
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

# Bind and listen
s.bind([HOST, PORT])
s.listen(5)

# Set server socket to blocking
s.setblocking(True)
clock = time.clock()

while True:
    # Accept a client socket
    clientsock, addr = s.accept()
    print("Accepted connection from ", addr)
    response = clientsock.recv(16)
    if(response == b'Ready'):
        print("Ready")
        clientsock.send(b'Ready')
        while True:
            try:
                while(response != b'Next'):
                    response = clientsock.recv(16)
                # Capture image
                img = sensor.snapshot()
                # Compress image to JPEG
                img_buf = img.compress(quality=imgCompression)

                clientsock.send(str(img_buf.size()))

                response = clientsock.recv(16)
                if(response == b'SizeOk'):
                    # Send image data to client
                    clientsock.sendall(img_buf)
                    response = clientsock.recv(16)
                    print(response)
                    # TODO send to robot
                else:
                    print("Error: ", e)
                    # Close client socket
                    clientsock.close()
                    time.sleep(1)
                    break
            except Exception as e:
                print("Error: ", e)
                # Close client socket
                clientsock.close()
                time.sleep(1)
                break
    else:
        print("error")
        clientsock.close()
        time.sleep(1)



