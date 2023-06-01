#from roadDetection import checkIntersections,checkSides
import roadDetection
import cv2
import numpy as np
import socket
import time
from signDetection import detectSign


#intersection variable
intersectionBacklogIndex = 0
intersectionBacklog = np.full(10, '', dtype=object)
intersectionFound = False
intersectionWait = False

#bord detected
LastSign = ""
signBacklogIndex = 0
signBacklog = np.full(10, '', dtype=object)

# IP address and port of the socket server
IP_ADDRESS = '192.168.137.41'
PORT = 8080

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((IP_ADDRESS, PORT))
client_socket.settimeout(1000)

try:
    client_socket.getpeername()
    #print("Socket is connected.")
    client_socket.sendall(b"ready")
except OSError:
    #print("Socket is not connected.")
    client_socket.close
    exit

#client_socket.send(b'ready')
response = client_socket.recv(16)
#print(response)
if(response != b'ready'):
    exit


while True:

    client_socket.sendall(b"next")

    # Receive image size from server

    while(1):
        try:
            # Attempt a small operation on the socket
            client_socket.getpeername()
            #print("Socket is still open.")
            break
        except socket.error:
            #print("Socket is closed.")
            client_socket.connect((IP_ADDRESS, PORT))
    
    img_size_str = client_socket.recv(16)
    decoded_string = img_size_str.decode('utf-8', 'ignore')
    substring = decoded_string[:5]
    img_size = int(substring)
    #print("img_size" + str(img_size))
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

    img = cv2.rotate(img, cv2.ROTATE_180)
    
    
    

    #img = roadDetection.readImage('C:\\VisionProject\\Pictures\\HVGA\\Weg\\00044.jpg',cv2.ROTATE_180)

    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # temp
    
    gray_blur_img = cv2.GaussianBlur(img,(5,5),0)


    #canny
    lowTreshold=100             #Any gradient values below this threshold are considered as not edges.
    highTreshold=200            #Any gradient values above this threshold are considered as edges.
    sobelKernel=apertureSize=3  #the size of the Sobel kernel used for gradient computation. It is an optional argument with a default value of 3.
    edges = cv2.Canny(gray_blur_img, lowTreshold, highTreshold, sobelKernel)
    

    usableHeight = 185
    imageWidth = 480



    #img = roadDetection.__cropImage(img,usableHeight,0,0,0)
    currentSign = detectSign(file=img)
    signBacklog[signBacklogIndex] = str(currentSign)
    signBacklogIndex = (signBacklogIndex + 1) % len(signBacklog)
    if(currentSign != "No Sign" and LastSign != currentSign):
        print("sign" + currentSign)
        cv2.waitKey(2000)
        #send data
        if(currentSign == "50 (0)"):
            client_socket.sendall(b"9")
        elif(currentSign == "Verboden auto (1)"):
            client_socket.sendall(b"8")
        elif(currentSign == "stop (2)"):
            client_socket.sendall(b"6")
        elif(currentSign == "Verboden in te rijden (3)"):
            client_socket.sendall(b"7")
        elif(currentSign == "Stoplicht rood (4)"):
            client_socket.sendall(b"10")
        elif(currentSign == "Stoplicht oranje (5)"):
            client_socket.sendall(b"11")
        elif(currentSign == "Stoplicht groen (6)"):
            client_socket.sendall(b"12")
        LastSign = currentSign
    else:

        correction = roadDetection.checkSides(middleOfScreen=(imageWidth/2),edges=edges,usableImageHeight=usableHeight,imgVisual=img)
        intersection,length = roadDetection.checkIntersections(edges=edges,usableImageHeight=usableHeight,imageWidth=imageWidth,imgVisual=img)
        print("length: "+ str(length))
        print("intersection: "+ str(intersection))   
            
        #only for visualizing
        #edges = roadDetection.__cropImage(edges,usableHeight,0,0,0)
        #cv2.imshow('Edges', edges)
        # end only for visualizing 

        #only for visualizing

        #cv2.imshow('img from nicla', img)
        # end only for visualizing 
    
        intersectionBacklog[intersectionBacklogIndex] = str(intersection)
        intersectionBacklogIndex = (intersectionBacklogIndex + 1) % len(intersectionBacklog)
        noAction = False
        #print(correction)

        if(intersection != "no intersection"):

            CountInter = 0
            for i in range(0, len(intersectionBacklog)):
                if(intersectionBacklog[i] != "no intersection" and intersectionBacklog[i] != "Error could not indentify intersection/corner" and intersectionBacklog[i] != ""):
                    CountInter +=1
            if(CountInter > 5):
                #print("intersectionFound!!!")
                intersectionFound = True


            if(intersectionWait == False and length > 55):
                print(correction)
                print("inter one time")
                if(correction == None or correction == -999):
                    client_socket.sendall(b"0")
                elif(correction < -50):
                    client_socket.sendall(b"185")
                    print("inter one right")
                elif(correction > -5):
                    client_socket.sendall(b"195")
                    print("inter one left")
                else:
                    client_socket.sendall(b"0")


                #client_socket.sendall(b"0")
                noAction = True
                intersectionWait = True
        
            elif(intersectionFound == True and length > 55):
                for i in range(0,len(intersectionBacklog)-1):
                    index = 0
                    if(intersectionBacklogIndex - i -1 < 0):
                        index = len(intersectionBacklog)-1 + intersectionBacklogIndex - i
                    else:
                        index = intersectionBacklogIndex - i

                    if(intersectionBacklog[index] != "no intersection" and intersectionBacklog[index] != "Error could not indentify intersection/corner" and intersectionBacklog[index] != ""):
                        currentInter = intersectionBacklog[index]
                        break
                intersectionBacklog = np.full(10, '', dtype=object)

                
                #print("currentInter " + str(currentInter))
                InverseLength = usableHeight-length
                intersectionFound = False
                byte_string = b""
                if(currentInter != "rightCorner" and currentInter != "leftCorner"):
                    user_input = input("Enter direction: ")
                    byte_string = b"" + user_input.encode() + b"|" + str(InverseLength).encode()
                elif(currentInter == "rightCorner"):
                    byte_string = b"right" + b"|" + str(InverseLength).encode()
                elif(currentInter == "leftCorner"):
                    byte_string = b"left" + b"|" + str(InverseLength).encode()
                client_socket.sendall(byte_string)
                noAction = True
                intersectionWait = False
            elif(intersectionFound == False and length > 55):
                client_socket.sendall(b"0")
                noAction = True


            #cv2.imshow('edges', edges)
            #cv2.waitKey(1)
            time.sleep(0.001)

            #cv2.destroyAllWindows()
        if(noAction == False):
            if(correction == None):
                #print("no line/not enough lines detected")
                client_socket.sendall(b"0")
                #print("sending data for car")
            elif(correction == -999):
                #print("error")
                client_socket.sendall(b"0")
                #print("sending data for car")
            elif(correction < -50):
                #print("right")
                client_socket.sendall(b"3")
                #print("sending data for car")
            elif(correction > -5):
                #print("left")
                client_socket.sendall(b"2")
                #print("sending data for car")
            else:
                #print("straight")
                client_socket.sendall(b"1")
                #print("sending data for car")
    

    #if(correction != -999):
    
    
