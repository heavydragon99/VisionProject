
import cv2
import numpy as np

def readImage(imgpath,rotateValue):
    img = cv2.imread(imgpath)
    img = cv2.rotate(img, rotateValue)
    return img

def cropImage(img,cropHeight,cropWidth):
    height, width = img.shape[:2]
    tempHeight = height-cropHeight
    tempWidth = width-cropWidth
    img = img[height-tempHeight:height, width-tempWidth:width]
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


def checkSideLines(edges):

    #hough
    rhoVar= 0.9              #the distance resolution of the accumulator in pixels. It determines the distance resolution of the detected lines.
    thetaVar =(np.pi/180)*2  #the angle resolution of the accumulator in radians. It determines the angular resolution of the detected lines.
    thresholdVar=60          #the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minThetaL =(np.pi/180)*0    # Beginning angel of hough (0 degrees)
    maxThetaL =(np.pi/180)*55   # ending angel of hough (55 degrees)

    #right
    minThetaR =(np.pi/180)*115  # Beginning angel of hough (115 degrees)
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
    rhoOffset = 10
    thetaOffset = 0.04

    if(allLines is not None):
    # delete lines that are to close to each other
        allLines = __gatherLines(allLines,rhoOffset,thetaOffset)
    #initializing lineXValues as array
        lineXValues = []
    #For each line the x value is calculated with the y = 0     
        for line in allLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # used for visualising on image (testing or for visualizing)
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

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
        cv2.imshow('Canny Edges', edges)
        cv2.imshow('Image from Socket', gray_img)

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
                    middle = left + lineXValues[2] / 2
                    correction = 160 - middle
                    return correction
                # 1l - 2r
                else:
                     right = (lineXValues[1] + lineXValues[2]) /2
                     middle = right + lineXValues[0] / 2
                     correction = 160 - middle
                     return correction
            # more then 4 lines
            elif(len(lineXValues) == 2 and linesL is not None and linesR is not None):
                print("2 lines 1l 1r")
                middle = lineXValues[0] + lineXValues[1] / 2
                correction = 160 - middle
                return correction
            elif(len(lineXValues) > 4):
                print("to many lines")
                return -999
            # other then above
            else:
                print("not enough lines")
                return -999

def checkIntesections(edges):
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
    thresholdVar=60          #the minimum number of votes (intersections in Hough space) required for a line to be detected. The higher the threshold, the fewer lines will be detected.
    
    #left
    minTheta =(np.pi/180)*70    # Beginning angel of hough (70 degrees)
    maxTheta =(np.pi/180)*110   # ending angel of hough (110 degrees)

    allLines = cv2.HoughLines(edges, rho=rhoVar, theta=thetaVar, threshold=thresholdVar,
                        min_theta=minTheta, max_theta=maxTheta)
    
    rhoOffset = 7.5
    thetaOffset = 0.021

    if(allLines is not None):
        allLines = __gatherLines(allLines,rhoOffset,thetaOffset)
        for line in allLines:
            rho, theta = line[0]
            # Change values to values for calculating lines
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # used for visualising on image (testing or for visualizing)
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(gray_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('Canny Edges', edges)
        cv2.imshow('Image from Socket', gray_img)

        
        if(len(allLines) >= 2):
            thetas = []
            for line in allLines:
                a = line[0][1]
                thetas.append(a)
            theta_mean = np.mean(thetas)
            theta_margin = 0.2
            filtered_lines = []
            for line in allLines:
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
            return True, distance
        else:
            return False, None
    else:
        return False, None


# Load image
img = readImage('C:\\VisionProject\\Pictures\\WegPlusBorden\\00041.jpg',cv2.ROTATE_180)
img = cropImage(img,140,0)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # temp

 #canny
lowTreshold=100             #Any gradient values below this threshold are considered as not edges.
highTreshold=200            #Any gradient values above this threshold are considered as edges.
sobelKernel=apertureSize=3  #the size of the Sobel kernel used for gradient computation. It is an optional argument with a default value of 3.
edges = cv2.Canny(img, lowTreshold, highTreshold, sobelKernel)


correction = checkSideLines(edges)
if(correction == None):
    print("no line/not enough lines detected")
elif(correction == -999):
    print("error")
elif(correction < -5):
    print("right")
elif(correction > 5):
    print("left")
else:
    print("straight")


print("intersection found?: " + str(checkIntesections(edges)))
print("Corner found?: " + str(checkCorner(edges)))
cv2.waitKey(0)

cv2.destroyAllWindows()
