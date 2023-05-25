import cv2
import numpy as np
import socket

# IP address and port of the socket server
IP_ADDRESS = '192.168.1.104'
PORT = 8080

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((IP_ADDRESS, PORT))
client_socket.settimeout(1000)

try:
    client_socket.getpeername()
    print("Socket is connected.")
    client_socket.sendall(b"ready")
except OSError:
    print("Socket is not connected.")
    client_socket.close
    exit

#client_socket.send(b'ready')
response = client_socket.recv(16)
print(response)
if(response != b'ready'):
    exit


while True:

    client_socket.sendall(b"next")

    # Receive image size from server
    img_size_str = client_socket.recv(16)
    decoded_string = img_size_str.decode('utf-8', 'ignore')
    substring = decoded_string[:5]
    img_size = int(substring)
    print("img_size" + str(img_size))
    client_socket.sendall(b"sizeok")

    # Receive image data from server
    img_buf = b''
    while len(img_buf) < img_size:
        chunk = client_socket.recv(img_size - len(img_buf))
        if not chunk:
            raise RuntimeError("socket connection broken")
        img_buf += chunk

    # Convert image buffer to numpy array
    img_arr = np.frombuffer(img_buf, dtype=np.uint8)

    # Decode image data to OpenCV Mat object
    img = cv2.imdecode(img_arr, cv2.IMREAD_GRAYSCALE)

    # TODO send data back on what robot needs to do
    client_socket.sendall(b"test")
    print("sending data for car")
    # Close socket
client_socket.close()


