
import cv2
import numpy as np

def readImage(imgpath,rotateValue):
    img = cv2.imread(imgpath)
    img = cv2.rotate(img, rotateValue)
    return img

def cropImage(img,beginCropHeight,beginCropWidth,endCropHeight,endCropWidth):
    height, width = img.shape[:2]
    begintempHeight = height-beginCropHeight
    begintempWidth = width-beginCropWidth
    endtempHeight = height-endCropHeight
    endtempWidth = width-endCropWidth
    print(width-begintempHeight)
    print(height-begintempWidth)
    print(endtempWidth)
    print(endtempWidth)

    
    img = img[int(height-begintempHeight):int(endtempHeight), int(width-begintempWidth):int(endtempWidth)]
    return img

def __gatherLines(allLines,rhoOffset,thetaOffset):
    indices_to_remove = []
    if(len(allLines != 0)):
        for i in range(0, len(allLines)): 
            rho, theta = allLines[i][0]
            for z in range(i+1, len(allLines)):
                temprho, temptheta = allLines[z][0]    
                if rho < temprho + rhoOffset and rho > temprho - rhoOffset and theta < temptheta + thetaOffset and theta > temptheta - thetaOffset:
                    indices_to_remove.append(i)
                    break
        allLines = np.delete(allLines, indices_to_remove, axis=0)
        return allLines

def checkRoadForLines(edges,rhoVar,thetaVar,minTheta,maxTheta,thresholdVar,rhoOffset,thetaOffset):
    
    lines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    if(lines is not None):
    # delete lines that are to close to each other
        lines = __gatherLines(lines,rhoOffset,thetaOffset)

    return lines

def checkSides(middleOfScreen,edges,usableImageHeight):
    img = cropImage(img,usableImageHeight,0,0,0)
    linesLeft = checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*0,maxTheta =(np.pi/180)*80,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    linesRight = checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*100,maxTheta =(np.pi/180)*180,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    allLines = None
    #check of left and right lines are found
    if(linesLeft is not None and linesRight is not None):
        allLines = np.concatenate((linesLeft, linesRight))
    elif(linesLeft is not None):
        allLines = linesLeft
    elif(linesRight is not None):
        allLines = linesRight
    
    # visualize
    # for line in allLines:
    #     rho, theta = line[0]
    #     # Change values to values for calculating lines
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000*(-b))
    #     y1 = int(y0 + 1000*(a))
    #     x2 = int(x0 - 1000*(-b))
    #     y2 = int(y0 - 1000*(a))
    #     cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow('Canny Edges', edges)
    # cv2.imshow('Image from Socket', gray_img)
    # end visualize

    #initialize variable
    lineXValues = []
    #For each line the x value is calculated with the y = 0     
    for line in allLines:
        rho, theta = line[0]
        # Change values to values for calculating lines
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho 
        # Calculate the x-value of the point where the line intersects the bottom edge of the image.
        # 1. Get the height of the image.
        # 2. Get the y-coordinate of the point where the line intersects the y-axis.
        # 3. Calculate the distance from y0 to the bottom edge of the image, minus 1 to account for 0-based indexing.
        # 4. Calculate the slope of the line, which is the negative of the tangent of theta (since a = cos(theta) and b = sin(theta)).
        # 5. Calculate the vertical distance from y0 to the bottom edge of the image, multiplied by the slope of the line, which gives the horizontal distance from the y-axis to the point where the line intersects the bottom edge of the image.
        # 6. Get the x-coordinate of the point where the line intersects the y-axis.
        # 7. Add the horizontal distance from the y-axis to the point where the line intersects the bottom edge of the image to the x-coordinate of the point where the line intersects the y-axis. This gives the x-coordinate of the point where the line intersects the bottom edge of the image.
        cvalueTest = int(x0 + (gray_img.shape[0]-y0-1)*(-b)/a) 
        lineXValues.append(cvalueTest)

    if(lineXValues is None):
        print("not enough lines")
        return -999
    # 4 lines 2r - 2l
    if(len(lineXValues) == 4):
        left = (lineXValues[0] + lineXValues[1]) /2
        right = (lineXValues[2] + lineXValues[3]) /2
        middle = left + right / 2
        correction = middleOfScreen - middle
        return correction
    # 3 lines
    elif(len(lineXValues) == 3):
        print("3 lines")
        # 2l - 1r
        if(len(linesL) == 2):
            left = (lineXValues[0] + lineXValues[1]) /2
            middle = (left + lineXValues[2]) / 2
            correction = middleOfScreen - middle
            return correction
        # 1l - 2r
        else:
                right = (lineXValues[1] + lineXValues[2]) /2
                middle = (right + lineXValues[0]) / 2
                correction = middleOfScreen - middle
                return correction
    # more then 4 lines
    elif(len(lineXValues) == 2 and linesL is not None and linesR is not None):
        print("2 lines 1l 1r")
        middle = (lineXValues[0] + lineXValues[1]) / 2
        correction = middleOfScreen - middle
        return correction
    elif(len(lineXValues) > 4):
        print("to many lines")
        return -999
    # other then above
    else:
        print("not enough lines")
        return -999
    
def checkIntersections(edges):
     
    # get lines to check if there is an intersection 
    lines = checkRoadForLines(edges,rhoVar=0.7,thetaVar =(np.pi/180)*0.5,minTheta =(np.pi/180)*70,maxTheta =(np.pi/180)*110,thresholdVar=75,rhoOffset = 8,thetaOffset = 0.04)
    
    #return when no intersectio or corner in detected
    if(lines is None or len(lines) < 2):
        return "no intersection"
    
    fourwayIntersection = True
    leftTIntersection = True
    rightTIntersection = True
    downTIntersection = True
    rightCorner = True
    leftCorner = True

    #check left side for verical lines to determine the X value
    linesLeft = checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*0,maxTheta =(np.pi/180)*80,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    
    #determine higest x value
    xHigh =0
    for line in linesLeft:
        rho, theta = line[0]
        # Change values to values for calculating lines
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        if(xHigh < x0):
            xHigh = x0
    print(xHigh)
    #crop image to be able to check left side of screen
    leftImage = cropImage(edges,0,0,0,320-xHigh)

    IntersectionLeft = checkRoadForLines(leftImage,rhoVar=0.5,thetaVar =(np.pi/180)*0.1,minTheta =(np.pi/180)*70,maxTheta =(np.pi/180)*110,thresholdVar=25,rhoOffset = 7.5,thetaOffset = 0.03)
    if(IntersectionLeft is None or len(IntersectionLeft) < 2):
        fourwayIntersection = False
        leftTIntersection = False
        downTIntersection = False
        leftCorner = False
    
    

    



def checkRoad2(edges,rhoVar,thetaVar,minThetaL,maxThetaL,minThetaR,maxThetaR,thresholdVar,rhoOffset,thetaOffset):
    #hough
    rhoVar= 0.9              #0.9#the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*2  #2 #the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=60          #60 #the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minThetaL =(np.pi/180)*0    # Beginning angel of hough (0 degrees)
    maxThetaL =(np.pi/180)*80   # ending angel of hough (55 degrees)

    #right
    minThetaR =(np.pi/180)*100  # Beginning angel of hough (115 degrees)
    maxThetaR =(np.pi/180)*180  # ending angel of hough (180 degrees)

    #left side
    linesL = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minThetaL, max_theta=maxThetaL)
    # right side
    linesR = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                            min_theta=minThetaR, max_theta=maxThetaR)
    allLines = None
    #check of left and right lines are found
    if(linesL is not None and linesR is not None):
        allLines = np.concatenate((linesL, linesR))
    elif(linesL is not None):
        allLines = linesL
    elif(linesR is not None):
        allLines = linesR

    # delete lines that are to close to each other
    rhoOffset = 10          #10
    thetaOffset = 0.07      #0.04

    if(allLines is not None):
    # delete lines that are to close to each other
        allLines = __gatherLines(allLines,rhoOffset,thetaOffset)
    
def checkSideLines(edges):

    allLines = checkRoad(edges=edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minThetaL =(np.pi/180)*0,maxThetaL =(np.pi/180)*80,minThetaR =(np.pi/180)*100,maxThetaR =(np.pi/180)*180,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.0)
    allLines = checkRoad(edges=edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minThetaL =(np.pi/180)*0,maxThetaL =(np.pi/180)*80,minThetaR =(np.pi/180)*100,maxThetaR =(np.pi/180)*180,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.0)

    # visualize
    # for line in allLines:
    #     rho, theta = line[0]
    #     # Change values to values for calculating lines
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000*(-b))
    #     y1 = int(y0 + 1000*(a))
    #     x2 = int(x0 - 1000*(-b))
    #     y2 = int(y0 - 1000*(a))
    #     cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow('Canny Edges', edges)
    # cv2.imshow('Image from Socket', gray_img)
    # end visualize

    #initialize variable
    lineXValues = []
    #For each line the x value is calculated with the y = 0     
    for line in allLines:
        rho, theta = line[0]
        # Change values to values for calculating lines
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho 
        # Calculate the x-value of the point where the line intersects the bottom edge of the image.
        # 1. Get the height of the image.
        # 2. Get the y-coordinate of the point where the line intersects the y-axis.
        # 3. Calculate the distance from y0 to the bottom edge of the image, minus 1 to account for 0-based indexing.
        # 4. Calculate the slope of the line, which is the negative of the tangent of theta (since a = cos(theta) and b = sin(theta)).
        # 5. Calculate the vertical distance from y0 to the bottom edge of the image, multiplied by the slope of the line, which gives the horizontal distance from the y-axis to the point where the line intersects the bottom edge of the image.
        # 6. Get the x-coordinate of the point where the line intersects the y-axis.
        # 7. Add the horizontal distance from the y-axis to the point where the line intersects the bottom edge of the image to the x-coordinate of the point where the line intersects the y-axis. This gives the x-coordinate of the point where the line intersects the bottom edge of the image.
        cvalueTest = int(x0 + (gray_img.shape[0]-y0-1)*(-b)/a) 
        lineXValues.append(cvalueTest)

    # visualising variable(testing or for visualizing)
    

    #calculating correction value
    for value in lineXValues:
        # 4 lines 2r - 2l
        if(len(lineXValues) == 4):
            left = (lineXValues[0] + lineXValues[1]) /2
            right = (lineXValues[2] + lineXValues[3]) /2
            middle = left + right / 2
            correction = 160 - middle
            return correction
        # 3 lines
        elif(len(lineXValues) == 3):
            print("3 lines")
            # 2l - 1r
            if(len(linesL) == 2):
                left = (lineXValues[0] + lineXValues[1]) /2
                middle = (left + lineXValues[2]) / 2
                correction = 160 - middle
                return correction
            # 1l - 2r
            else:
                    right = (lineXValues[1] + lineXValues[2]) /2
                    middle = (right + lineXValues[0]) / 2
                    correction = 160 - middle
                    return correction
        # more then 4 lines
        elif(len(lineXValues) == 2 and linesL is not None and linesR is not None):
            print("2 lines 1l 1r")
            middle = (lineXValues[0] + lineXValues[1]) / 2
            correction = 160 - middle
            return correction
        elif(len(lineXValues) > 4):
            print("to many lines")
            return -999
        # other then above
        else:
            print("not enough lines")
            return -999

def checkIntesections2(edges):
    #hough
    rhoVar= 0.7              #the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*0.5#the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=75          #the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minTheta =(np.pi/180)*70    # Beginning angel of hough (70 degrees)
    maxTheta =(np.pi/180)*110   # ending angel of hough (110 degrees)

    allLines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    
    rhoOffset = 8
    thetaOffset = 0.04

    if(allLines is not None):
    # delete lines that are to close to each other
        allLines = __gatherLines(allLines,rhoOffset,thetaOffset)
        i = 0
        found_match = False
        while i < len(allLines) and not found_match:
            rho, theta = allLines[i][0]
            for j in range(i+1, len(allLines)):
                if allLines[j][0][1] == theta:
                    found_match = True
                    break
            i += 1
        

        # used for visualising on image (testing or for visualizing)
        for line in allLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho


           
            # used for visualising on image (testing or for visualizing)
            # x1 = int(x0 + 1000*(-b))
            # y1 = int(y0 + 1000*(a))
            # x2 = int(x0 - 1000*(-b))
            # y2 = int(y0 - 1000*(a))
            # cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # visualising variable(testing or for visualizing)
        cv2.imshow('Canny Edges', edges)
        cv2.imshow('Image from Socket', gray_img)

        return found_match

def checkCorner(edges):
    #hough
    rhoVar= 0.5              #the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*0.1#the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=50          #65#the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minTheta =(np.pi/180)*70    # Beginning angel of hough (70 degrees)
    maxTheta =(np.pi/180)*110   # ending angel of hough (110 degrees)

    HorizontalLines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    
    rhoOffset = 7.5
    thetaOffset = 0.021

    if(HorizontalLines is not None):
        HorizontalLines = __gatherLines(HorizontalLines,rhoOffset,thetaOffset)
        for line in HorizontalLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # used for visualising on image (testing or for visualizing)
            # x1 = int(x0 + 1000*(-b))
            # y1 = int(y0 + 1000*(a))
            # x2 = int(x0 - 1000*(-b))
            # y2 = int(y0 - 1000*(a))
            # cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('Canny Edges', edges)
        cv2.imshow('Image from Socket', gray_img)

        
        if(len(HorizontalLines) >= 2):
            thetas = []
            for line in HorizontalLines:
                a = line[0][1]
                thetas.append(a)
            theta_mean = np.mean(thetas)
            theta_margin = 0.2
            filtered_lines = []
            for line in HorizontalLines:
                a = line[0][1]
                if abs(a - theta_mean) < theta_margin:
                    b = line[0][0]
                    sin_theta = np.sin(a)
                    cos_theta = np.cos(a)
                    y = (b - 160*cos_theta) / sin_theta
                    filtered_lines.append(y)
            if filtered_lines:
                distance = 140 - np.mean(filtered_lines)
            else:
                distance = None
            checkIntersection(edges)
            return True, distance
        else:
            return False, None
    else:
        return False, None

def checkIntersection3(edges):
    #hough
    rhoVar= 0.9              #0.9#the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*2  #2 #the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=60          #60 #the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minTheta =(np.pi/180)*0    # Beginning angel of hough (70 degrees)
    maxTheta =(np.pi/180)*80   # ending angel of hough (110 degrees)

    VerticalLines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    print("test")
    print(VerticalLines)
    rhoOffset = 7.5
    thetaOffset = 0.021
    if(VerticalLines is not None):
        VerticalLines = __gatherLines(VerticalLines,rhoOffset,thetaOffset)
        xHigh = 0
        for line in VerticalLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            if(xHigh < x0):
                xHigh = x0
            # used for visualising on image (testing or for visualizing)
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(xHigh)
        test = cropImage(edges,0,0,0,320-xHigh)
        cv2.imshow('Canny Edges', edges)
        cv2.imshow('test', test)
        cv2.imshow('Image from Socket', gray_img)



    #hough
    rhoVar= 0.5              #the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*0.1#the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=25          #65#the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minTheta =(np.pi/180)*70    # Beginning angel of hough (70 degrees)
    maxTheta =(np.pi/180)*110   # ending angel of hough (110 degrees)

    HorizontalLines = cv2.HoughLines(test, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    print("test")
    print(HorizontalLines)
    rhoOffset = 7.5
    thetaOffset = 0.03
    if(HorizontalLines is not None):
        HorizontalLines = __gatherLines(HorizontalLines,rhoOffset,thetaOffset)
        xHigh = 0
        for line in HorizontalLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            if(xHigh < x0):
                xHigh = x0
            # used for visualising on image (testing or for visualizing)
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(xHigh)
        #test = cropImage(edges,0,0,0,320-xHigh)
        cv2.imshow('Canny Edges', edges)
        #cv2.imshow('test', test)
        cv2.imshow('Image from Socket', gray_img)

def checkTIntersection(edges):
    #hough
    rhoVar= 0.5              #the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*0.1#the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=25          #65#the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minTheta =(np.pi/180)*70    # Beginning angel of hough (70 degrees)
    maxTheta =(np.pi/180)*110   # ending angel of hough (110 degrees)

    HorizontalLines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    print("test")
    print(HorizontalLines)
    rhoOffset = 7.5
    thetaOffset = 0.03
    if(HorizontalLines is not None):
        HorizontalLines = __gatherLines(HorizontalLines,rhoOffset,thetaOffset)
        xHigh = 0
        for line in HorizontalLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            if(xHigh < x0):
                xHigh = x0
            # used for visualising on image (testing or for visualizing)
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(xHigh)
        #test = cropImage(edges,0,0,0,320-xHigh)
        cv2.imshow('Canny Edges', edges)
        #cv2.imshow('test', test)
        cv2.imshow('Image from Socket', gray_img)        
        










# Load image
img = readImage('C:\\VisionProject\\Pictures\\WegFout(Test)\\rtIntersection\\00005.jpg',cv2.ROTATE_180)
#img = readImage('C:\\VisionProject\\Pictures\\WegPlusBorden\\00038.jpg',cv2.ROTATE_180)
#img = cropImage(img,140,0,0,0)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # temp


# Creating the kernel(2d convolution matrix)
kernel1 = np.ones((3, 3), np.float32)/9
  

img_test2 = cv2.GaussianBlur(gray_img,(3,3),0)
cv2.imshow('img_test', img_test2)

 #canny
lowTreshold=100             #Any gradient values below this threshold are considered as not edges.
highTreshold=200            #Any gradient values above this threshold are considered as edges.
sobelKernel=apertureSize=3  #the size of the Sobel kernel used for gradient computation. It is an optional argument with a default value of 3.
edges = cv2.Canny(img_test2, lowTreshold, highTreshold, sobelKernel)

correction = checkSides(middleOfScreen=160,edges=edges,usableImageHeight=140)
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

cv2.waitKey(0)

cv2.destroyAllWindows()
