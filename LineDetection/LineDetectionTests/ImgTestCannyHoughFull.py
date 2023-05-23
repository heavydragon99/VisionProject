
import cv2
import numpy as np
import sys

def __drawLines(lines):
    #visualize
    if(lines is not None):
        for line in lines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('Image from Socket', gray_img)
    # end visualize 


def readImage(imgpath,rotateValue):
    img = cv2.imread(imgpath)
    img = cv2.rotate(img, rotateValue)
    return img

def __cropImage(img,beginCropHeight,beginCropWidth,endCropHeight,endCropWidth):
    height, width = img.shape[:2]
    begintempHeight = height-beginCropHeight
    begintempWidth = width-beginCropWidth
    endtempHeight = height-endCropHeight
    endtempWidth = width-endCropWidth
    #print(width-begintempHeight)
    #print(height-begintempWidth)
    #print(endtempWidth)
    #print(endtempHeight)

    
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

def __checkRoadForLines(edges,rhoVar,thetaVar,minTheta,maxTheta,thresholdVar,rhoOffset,thetaOffset):
    
    lines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    if(lines is not None):
    # delete lines that are to close to each other
        lines = __gatherLines(lines,rhoOffset,thetaOffset)

    return lines

def checkSides(middleOfScreen,edges,usableImageHeight):
    #uses 2 times hough
    edges = __cropImage(edges,usableImageHeight,0,0,0)
    linesLeft = __checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*0,maxTheta =(np.pi/180)*80,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    linesRight = __checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*100,maxTheta =(np.pi/180)*180,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    allLines = None
    #check of left and right lines are found
    if(linesLeft is not None and linesRight is not None):
        allLines = np.concatenate((linesLeft, linesRight))
    elif(linesLeft is not None):
        allLines = linesLeft
    elif(linesRight is not None):
        allLines = linesRight
    
    

    # visualize
    #__drawLines(allLines);
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
        # calculate the x-value of the point where the line intersects the bottom edge of the image.
        # 1. get the height of the image.
        # 2. get the y-coordinate of the point where the line intersects the y-axis.
        # 3. calculate the distance from y0 to the bottom edge of the image, minus 1 to account for 0-based indexing.
        # 4. calculate the slope of the line, which is the negative of the tangent of theta (since a = cos(theta) and b = sin(theta)).
        # 5. calculate the vertical distance from y0 to the bottom edge of the image, multiplied by the slope of the line, which gives the horizontal distance from the y-axis to the point where the line intersects the bottom edge of the image.
        # 6. get the x-coordinate of the point where the line intersects the y-axis.
        # 7. add the horizontal distance from the y-axis to the point where the line intersects the bottom edge of the image to the x-coordinate of the point where the line intersects the y-axis. This gives the x-coordinate of the point where the line intersects the bottom edge of the image.
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
        if(len(linesLeft) == 2):
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
    elif(len(lineXValues) == 2 and linesLeft is not None and linesRight is not None):
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
    
def checkIntersections(edges,usableImageHeight,imageWidth):
    #uses 6 thimes Hough
    edges = __cropImage(edges,usableImageHeight,0,0,0)
    # get lines to check if there is an intersection 
    lines = __checkRoadForLines(edges,rhoVar=0.7,thetaVar =(np.pi/180)*0.5,minTheta =(np.pi/180)*70,maxTheta =(np.pi/180)*110,thresholdVar=60,rhoOffset = 8,thetaOffset = 0.04)
    
    #return when no intersectio or corner in detected
    if(lines is None):
        return "no intersection"
    
    if(len(lines) < 2):
        #temp
        #__drawLines(lines)
        return "no intersection"
    
    # visualize
    #__drawLines(lines)
    # end visualize    
    
    fourwayIntersection = True
    leftTIntersection = True
    rightTIntersection = True
    downTIntersection = True
    rightCorner = True
    leftCorner = True

    #check left side for verical lines to determine the X value
    linesLeft = __checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*0,maxTheta =(np.pi/180)*80,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    # visualize
    #__drawLines(linesLeft)
    # end visualize 

    #determine higest x value
    if(linesLeft is not None):
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
        #print("xHigh: "+ str(xHigh))
        #crop image to be able to check left side of screen
        leftImage = __cropImage(edges,0,0,0,imageWidth-xHigh)

        IntersectionLeft = __checkRoadForLines(leftImage,rhoVar=0.5,thetaVar =(np.pi/180)*0.1,minTheta =(np.pi/180)*70,maxTheta =(np.pi/180)*110,thresholdVar=25,rhoOffset = 7.5,thetaOffset = 0.03)
        if(IntersectionLeft is None or len(IntersectionLeft) < 2):
            fourwayIntersection = False
            leftTIntersection = False
            downTIntersection = False
            leftCorner = False
    else:
        fourwayIntersection = False
        leftTIntersection = False
        downTIntersection = False
        leftCorner = False


    yHigh = sys.maxsize
    for line in lines:
        rho, theta = line[0]
        # Change values to values for calculating lines
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        if(yHigh > y0):
            yHigh = y0
    #print("yHigh: "+ str(yHigh))

    # visualize
    #__drawLines(IntersectionLeft)
    # end visualize 
   
    upImage = __cropImage(edges,0,0,100-yHigh,0)
    IntersectionUpLeft = __checkRoadForLines(upImage,rhoVar=0.5,thetaVar =(np.pi/180)*0.5,minTheta =(np.pi/180)*0,maxTheta =(np.pi/180)*80,thresholdVar=25,rhoOffset = 7.5,thetaOffset = 0.03)
    IntersectionUpRight = __checkRoadForLines(upImage,rhoVar=0.5,thetaVar =(np.pi/180)*0.5,minTheta =(np.pi/180)*100,maxTheta =(np.pi/180)*180,thresholdVar=25,rhoOffset = 7.5,thetaOffset = 0.03)
    if(IntersectionUpLeft is None or IntersectionUpRight is None):
        fourwayIntersection = False
        leftTIntersection = False
        rightTIntersection = False
    
    # visualize
    #__drawLines(IntersectionUpLeft)
    #__drawLines(IntersectionUpRight)
    # end visualize 


    #check right side
    #TODO: test if needed
    linesRight = __checkRoadForLines(edges,rhoVar=0.9,thetaVar =(np.pi/180)*2,minTheta =(np.pi/180)*100,maxTheta =(np.pi/180)*180,thresholdVar=60,rhoOffset = 10,thetaOffset = 0.07)
    
    # visualize
    #__drawLines(linesRight)
    # end visualize 
    
    if(linesRight is not None):
        xLow = sys.maxsize
        for line in linesRight:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            if(xLow > x0):
                xLow = x0
        #print("xLow: "+ str(xLow))
        rightImage = __cropImage(edges,0,imageWidth-xLow,0,0)
        #cv2.imshow('rightImage', rightImage)
        IntersectionRight = __checkRoadForLines(rightImage,rhoVar=0.5,thetaVar =(np.pi/180)*0.1,minTheta =(np.pi/180)*70,maxTheta =(np.pi/180)*110,thresholdVar=25,rhoOffset = 7.5,thetaOffset = 0.03)
        
        # visualize
        #__drawLines(IntersectionRight)
        # end visualize 
        
        if(IntersectionRight is None or len(IntersectionRight) < 2):
            fourwayIntersection = False
            rightTIntersection = False
            downTIntersection = False
            rightCorner = False
    else:
        fourwayIntersection = False
        rightTIntersection = False
        downTIntersection = False
        rightCorner = False
    
    if(fourwayIntersection == True):
        return "fourwayIntersection"
    elif(leftTIntersection == True):
        return "leftTIntersection"
    elif(rightTIntersection == True):
        return "rightTIntersection"
    elif(downTIntersection == True):
        return "downTIntersection"
    elif(rightCorner == True):
        return "rightCorner"
    elif(leftCorner == True):
        return "leftCorner"
    else:
        return "Error could not indentify intersection/corner"



# ------------------------------------main--------------------------------------------- #

# Load image
#img = readImage('C:\\VisionProject\\Pictures\\WegFout(Test)\\rtIntersection\\00005.jpg',cv2.ROTATE_180)
img = readImage('C:\\VisionProject\\Pictures\\WegPlusBorden\\00016.jpg',cv2.ROTATE_180)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # temp
  
gray_blur_img = cv2.GaussianBlur(gray_img,(3,3),0)


 #canny
lowTreshold=100             #Any gradient values below this threshold are considered as not edges.
highTreshold=200            #Any gradient values above this threshold are considered as edges.
sobelKernel=apertureSize=3  #the size of the Sobel kernel used for gradient computation. It is an optional argument with a default value of 3.
edges = cv2.Canny(gray_blur_img, lowTreshold, highTreshold, sobelKernel)

#only for visualizing
gray_img = __cropImage(gray_img,140,0,0,0)
cv2.imshow('Image from Socket', gray_img)
# end only for visualizing 

correction = checkSides(middleOfScreen=160,edges=edges,usableImageHeight=140)

#only for visualizing
#edges = __cropImage(edges,140,0,0,0)
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

print(checkIntersections(edges=edges,usableImageHeight=140,imageWidth=320))

cv2.waitKey(0)

cv2.destroyAllWindows()
