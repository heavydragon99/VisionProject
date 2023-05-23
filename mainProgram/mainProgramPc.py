import roadDetection
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
        #print("image data")
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

    #cv2.imshow('img from nicla', img)
    #img = roadDetection.readImage('C:\\VisionProject\\Pictures\\HVGA\\Weg\\00044.jpg',cv2.ROTATE_180)

    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # temp
    
    gray_blur_img = cv2.GaussianBlur(img,(5,5),0)


    #canny
    lowTreshold=100             #Any gradient values below this threshold are considered as not edges.
    highTreshold=200            #Any gradient values above this threshold are considered as edges.
    sobelKernel=apertureSize=3  #the size of the Sobel kernel used for gradient computation. It is an optional argument with a default value of 3.
    edges = cv2.Canny(gray_blur_img, lowTreshold, highTreshold, sobelKernel)
    #cv2.imshow('edges', edges)

    usableHeight = 185
    imageWidth = 420

    correction = roadDetection.checkSides(middleOfScreen=(imageWidth/2),edges=edges,usableImageHeight=usableHeight)
    correction = 0
    #only for visualizing
    edges = roadDetection.__cropImage(edges,usableHeight,0,0,0)
    #cv2.imshow('Edges', edges)
    # end only for visualizing 

    print(correction)
    if(correction == None):
        print("no line/not enough lines detected")
    elif(correction == -999):
        print("error")
    elif(correction < -20):
        print("right")
    elif(correction > 20):
        print("left")
    else:
        print("straight")

    #if(correction != -999):
    print(roadDetection.checkIntersections(edges=edges,usableImageHeight=usableHeight,imageWidth=imageWidth))

    #cv2.waitKey(100)

    #cv2.destroyAllWindows()
