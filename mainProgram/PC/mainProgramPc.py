#from roadDetection import checkIntersections,checkSides
import roadDetection
import cv2
import numpy as np
import socket
import time
from signDetection import detectSign, classes


#intersection variable
intersectionBacklogIndex = 0
intersectionBacklog = np.full(10, '', dtype=object)
intersectionFound = False
intersectionWait = False

#bord detected
LastSign = ""
signBacklogIndex = 0
signBacklog = np.full(3, '', dtype=object)

# Wi-Fi variable
IP_ADDRESS = '192.168.137.66'
PORT = 8080
Connected = True






def wifiMessage(messageSelect,data=None,size=0):
    print("wifi")
    connectionStatus = False
    dataReturn = None
    try:
        connectionStatus = True
        if(messageSelect == 0):
            client_socket.getpeername()
        elif(messageSelect == 1):
            client_socket.sendall(data)
        elif(messageSelect == 2):
            
            dataReturn = client_socket.recv(size)
            #print("dataReturn" + str(dataReturn))
        else:
            client_socket.close 
            connectionStatus = False
    except OSError:
        client_socket.close 
        connectionStatus = False
    
    if(dataReturn is not None and dataReturn != ""):
        #print("dataReturn2 " + str(dataReturn))
        return connectionStatus,dataReturn
    else:
        return connectionStatus,None

while True:
     # Create socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("init")
    # Connect to server
    try:
        print("waiting")
        client_socket.connect((IP_ADDRESS, PORT))
        client_socket.settimeout(1000)
    except OSError:
        print("could not connected")
        client_socket.close 
        connectionStatus = False
        time.sleep(1)
    Connected = wifiMessage(messageSelect=0)
    print("Connected1" + str(Connected))
    Connected = wifiMessage(messageSelect=1,data=b"ready")
    print("Connected2" + str(Connected))
    Connected,response = wifiMessage(messageSelect=2,size=16)   
    print("Connected3" + str(Connected)) 
    print("response " + str(response))
    if(response != b'ready' and Connected == True):
        print("int not ready")
        client_socket.close
        Connected = False
    print("main loop")
    while Connected:
        Connected = wifiMessage(1,b"next")
        print("main loop next")
        if(not Connected):
            break

        # Receive image size from server        
        #img_size_str = client_socket.recv(16)
        Connected,img_size_str = wifiMessage(2,"",16)
        print("main loop receive size")
        if(not Connected):
            break


        decoded_string = img_size_str.decode('utf-8', 'ignore')
        print("main loop decode")
        substring = decoded_string[:5]
        print("main loop decode 2")
        if(substring == ""):
            Connected = False
            break
        print("main loop decode 3")
        img_size = int(substring)
        #print("img_size" + str(img_size))
        Connected = wifiMessage(1,b"sizeok")
        print("main loop sizeok")
        if(not Connected):
            break

        # Receive image data from server
        img_buf = b''
        while len(img_buf) < img_size:
            #print("image data")
            #chunk = client_socket.recv(img_size - len(img_buf))
            Connected,chunk = wifiMessage(2,"",img_size - len(img_buf))
            if(not Connected):
                break

            if not chunk:
                Connected = False
                break
            img_buf += chunk
        if(not Connected):
            break
        # Convert image buffer to numpy array
        img_arr = np.frombuffer(img_buf, dtype=np.uint8)

        # Decode image data to OpenCV Mat object
        try:
            img = cv2.imdecode(img_arr, cv2.IMREAD_GRAYSCALE)

            img = cv2.rotate(img, cv2.ROTATE_180)
        except OSError:
            client_socket.close 
            connectionStatus = False
            break

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
        detectedSign = detectSign(file=img)
        currentSign = ""
        signBacklog[signBacklogIndex] = str(detectedSign)
        signBacklogIndex = (signBacklogIndex + 1) % len(signBacklog)
        bordCountArray = [0,0,0,0,0,0,0,0]
        for i in signBacklog:
            for j in classes:
                if i == classes[j]:
                    bordCountArray[j] += 1
                    break

        currentSign = classes[bordCountArray.index(max(bordCountArray))]
        #print("Current most detected sign is: " + currentSign)

        if(LastSign != currentSign and currentSign != "No Sign"):
            #send
            print("Current most detected sign is: " + currentSign)
            if(currentSign == "50 (0)"):
                Connected = wifiMessage(1,b"9")
                if(not Connected):
                    break
                #print("9")
            elif(currentSign == "Verboden auto (1)"):
                Connected = wifiMessage(1,b"8")
                if(not Connected):
                    break
                #print("8")
            elif(currentSign == "stop (2)"):
                Connected = wifiMessage(1,b"6")
                if(not Connected):
                    break
                #print("6")
            elif(currentSign == "Verboden in te rijden (3)"):
                Connected = wifiMessage(1,b"7")
                if(not Connected):
                    break
                #print("7")
            elif(currentSign == "Stoplicht rood (4)"):
                Connected = wifiMessage(1,b"10")
                if(not Connected):
                    break
                #print("10")
            elif(currentSign == "Stoplicht oranje (5)"):
                Connected = wifiMessage(1,b"11")
                if(not Connected):
                    break
                #print("11")
            elif(currentSign == "Stoplicht groen (6)"):
                Connected = wifiMessage(1,b"12")
                if(not Connected):
                    break  
                #print("12")       
        else:

            correction = roadDetection.checkSides(middleOfScreen=(imageWidth/2),edges=edges,usableImageHeight=usableHeight,imgVisual=img)
            intersection,length = roadDetection.checkIntersections(edges=edges,usableImageHeight=usableHeight,imageWidth=imageWidth,imgVisual=img)
            #print("length: "+ str(length))
            #print("intersection: "+ str(intersection))   
                
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

            if(intersection != "no intersection" or intersectionWait == True):

                CountInter = 0
                for i in range(0, len(intersectionBacklog)):
                    if(intersectionBacklog[i] != "no intersection" and intersectionBacklog[i] != "Error could not indentify intersection/corner" and intersectionBacklog[i] != ""):
                        CountInter +=1
                if(CountInter > 2):
                    #print(CountInter)
                    #print("intersectionFound!!!")
                    intersectionFound = True


                if(intersectionWait == False and length > 50):
                    #print(correction)
                    #print("inter one time")
                    if(correction == None or correction == -999):
                        Connected = wifiMessage(1,b"0")
                        if(not Connected):
                            break
                    elif(correction < -40):
                        Connected = wifiMessage(1,b"185")
                        if(not Connected):
                            break
                        #print("inter one right")
                    elif(correction > -15):
                        Connected = wifiMessage(1,b"195")
                        if(not Connected):
                            break
                        #print("inter one left")
                    else:
                        Connected = wifiMessage(1,b"0")
                        if(not Connected):
                            break


                    #client_socket.sendall(b"0")
                    noAction = True
                    intersectionWait = True
                
                elif(intersectionWait == True):
                    #print("intersectionWait" + str(intersectionWait))
                    last_added_index = (intersectionBacklogIndex - 1) % len(intersectionBacklog)
                    last_added_value = intersectionBacklog[last_added_index]
                    previous_value = ""

                    while last_added_value in ["no intersection", "Error could not identify intersection/corner", ""] or previous_value in ["no intersection", "Error could not identify intersection/corner", ""]:
                        previous_value = last_added_value
                        last_added_index = (last_added_index - 1) % len(intersectionBacklog)
                        last_added_value = intersectionBacklog[last_added_index]

                    #print("last_added_value" + str(last_added_value))
                    currentInter = last_added_value
                    # for i in range(0,len(intersectionBacklog)-1):
                    #     index = 0
                    #     if(intersectionBacklogIndex - i -1 < 0):
                    #         index = len(intersectionBacklog)-1 + intersectionBacklogIndex - i
                    #     else:
                    #         index = intersectionBacklogIndex - i

                    #     if(intersectionBacklog[index] != "no intersection" and intersectionBacklog[index] != "Error could not indentify intersection/corner" and intersectionBacklog[index] != ""):
                    #         currentInter = intersectionBacklog[index]
                    #         break



                    intersectionBacklog = np.full(10, '', dtype=object)

                    
                    #print("currentInter " + str(currentInter))
                    InverseLength = usableHeight-length
                    intersectionFound = False
                    byte_string = b""
                    if(currentInter != "rightCorner" and currentInter != "leftCorner"):
                        user_input = input("Enter direction: ")
                        #user_input = "up"
                        byte_string = b"" + user_input.encode() + b"|" + str(InverseLength).encode()
                    elif(currentInter == "rightCorner"):
                        byte_string = b"right" + b"|" + str(InverseLength).encode()
                    elif(currentInter == "leftCorner"):
                        byte_string = b"left" + b"|" + str(InverseLength).encode()
                    Connected = wifiMessage(1,byte_string)
                    if(not Connected):
                        break
                    noAction = True
                    intersectionWait = False
                elif(intersectionFound == False and length > 50):
                    Connected = wifiMessage(1,b"0")
                    if(not Connected):
                        break
                    noAction = True


                #cv2.imshow('edges', edges)
                #cv2.waitKey(1)
                time.sleep(0.001)

                #cv2.destroyAllWindows()
            if(noAction == False):
                if(correction == None):
                    #print("no line/not enough lines detected")
                    Connected = wifiMessage(1,b"0")
                    if(not Connected):
                        break
                    #print("sending data for car")
                elif(correction == -999):
                    #print("error")
                    Connected = wifiMessage(1,b"0")
                    if(not Connected):
                        break
                    #print("sending data for car")
                elif(correction < -55):
                    #print("right")
                    Connected = wifiMessage(1,b"3")
                    if(not Connected):
                        break
                    #print("sending data for car")
                elif(correction > 0):
                    #print("left")
                    Connected = wifiMessage(1,b"2")
                    if(not Connected):
                        break
                    #print("sending data for car")
                else:
                    #print("straight")
                    Connected = wifiMessage(1,b"1")
                    if(not Connected):
                        break
                    #print("sending data for car")
        
        LastSign = currentSign
        #if(correction != -999):
        print("end main loop")
        
        
