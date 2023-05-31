# Load the trained model to classify sign
from keras.models import load_model
import cv2
import numpy as np
#import matplotlib.pyplot as plt
from math import sqrt
#from skimage.feature import blob_dog, blob_log, blob_doh
import imutils

min_size_components = 300
similitary_contour_with_circle = 0.60

model = load_model('traffic_classifier_7bordenv3.h5')

# Dictionary to label all traffic signs class.
classes = {0: 'None',
           1: '50 (0)',
           2: 'Verboden auto (1)',
           3: 'stop (2)',
           4: 'Verboden in te rijden (3)',
           5: 'Stoplicht rood (4)',
           6: 'Stoplicht oranje (5)',
           7: 'Stoplicht groen (6)'}


def classify(image):
    global label_packed
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    image = cv2.resize(image,(30,30))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    pred_probs = model.predict(image)  # Get predicted probabilities for each class
    pred = np.argmax(pred_probs)  # Get the class label with highest probability using np.argmax

    max_prob = pred_probs[0, pred]  # Retrieve the predicted probability for the highest class
    confidence_percent = max_prob * 100  # Calculate the confidence percentage
    print(confidence_percent)

    if confidence_percent > 80:
        sign = classes[pred + 1]
    else:
        sign=classes[0]    
    return sign


### Preprocess image

def contrastLimit(image):
    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(image)
    return equalized_image


def LaplacianOfGaussian(image):
    LoG_image = cv2.GaussianBlur(image, (5,5), 0)           # paramter 
    gray = LoG_image
    LoG_image = cv2.Laplacian( gray, cv2.CV_8U,3,3,2)       # parameter
    LoG_image = cv2.convertScaleAbs(LoG_image)
    return LoG_image
    
def binarization(image):
    thresh = cv2.threshold(image,45,255,cv2.THRESH_BINARY)[1]
    #thresh = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return thresh

def preprocess_image(image):
    image = contrastLimit(image)
    image = LaplacianOfGaussian(image)
    image = binarization(image)
    return image

# Find Signs
def removeSmallComponents(image, threshold):
    #find all your connected components (white blobs in your image)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    sizes = stats[1:, -1]; nb_components = nb_components - 1

    img2 = np.zeros((output.shape),dtype = np.uint8)
    #for every component in the image, you keep it only if it's above threshold
    for i in range(0, nb_components):
        if sizes[i] >= threshold:
            img2[output == i + 1] = 255
    return img2

def findContour(image):
    #find contours in the thresholded image
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE    )
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts

def contourIsSign(perimeter, centroid, threshold):
    #  perimeter, centroid, threshold
    # # Compute signature of contour
    result=[]
    for p in perimeter:
        p = p[0]
        distance = sqrt((p[0] - centroid[0])**2 + (p[1] - centroid[1])**2)
        result.append(distance)
    max_value = max(result)
    signature = [float(dist) / max_value for dist in result ]
    # Check signature of contour.
    temp = sum((1 - s) for s in signature)
    temp = temp / len(signature)
    if temp < threshold: # is  the sign
        return True, max_value + 2
    else:                 # is not the sign
        return False, max_value + 2

#crop sign 
def cropContour(image, center, max_distance):
    width = image.shape[1]
    height = image.shape[0]
    top = max([int(center[0] - max_distance), 0])
    bottom = min([int(center[0] + max_distance + 1), height-1])
    left = max([int(center[1] - max_distance), 0])
    right = min([int(center[1] + max_distance+1), width-1])
    #(left, right, top, bottom)
    return image[left:right, top:bottom]

def cropSign(image, coordinate):
    width = image.shape[1]
    height = image.shape[0]
    top = max([int(coordinate[0][1]), 0])
    bottom = min([int(coordinate[1][1]), height-1])
    left = max([int(coordinate[0][0]), 0])
    right = min([int(coordinate[1][0]), width-1])
    #print(top,left,bottom,right)
    return image[top:bottom,left:right]


def findLargestSign(image, contours, threshold, distance_theshold):
    max_distance = 0
    coordinate = None
    sign = None
    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        is_sign, distance = contourIsSign(c, [cX, cY], 1-threshold)
        if is_sign and distance > max_distance and distance > distance_theshold:
            max_distance = distance
            coordinate = np.reshape(c, [-1,2])
            left, top = np.amin(coordinate, axis=0)
            right, bottom = np.amax(coordinate, axis = 0)
            coordinate = [(left-2,top-2),(right+3,bottom+1)]
            sign = cropSign(image,coordinate)
    return sign


def findSigns(image, contours, threshold, distance_theshold):
    signs = []
    coordinates = []
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        is_sign, max_distance = contourIsSign(c, [cX, cY], 1-threshold)
        if is_sign and max_distance > distance_theshold:
            sign = cropContour(image, [cX, cY], max_distance)
            signs.append(sign)
            coordinate = np.reshape(c, [-1,2])
            top, left = np.amin(coordinate, axis=0)
            right, bottom = np.amax(coordinate, axis = 0)
            coordinates.append([(top-2,left-2),(right+1,bottom+1)])
    return signs, coordinates

def localization(image, min_size_components, similitary_contour_with_circle):
    original_image = image.copy()
    binary_image = preprocess_image(image)

    binary_image = removeSmallComponents(binary_image, min_size_components)

    cv2.imshow('Binary',binary_image)
    contours = findContour(binary_image)
    sign = findLargestSign(original_image, contours, similitary_contour_with_circle, 15)

    return sign

def remove_line(img):
    gray = img.copy()
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength = 5
    maxLineGap = 3
    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
    mask = np.ones(img.shape[:2], dtype="uint8") * 255
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(mask,(x1,y1),(x2,y2),(0,0,0),2)
    return cv2.bitwise_and(img, img, mask=mask)

def detectSign(file):
    sourceImage = file
    sourceImage = cv2.rotate(sourceImage,cv2.ROTATE_180)            #Rotate it so the it has the right orientation
    sourceImage = cv2.cvtColor(sourceImage, cv2.COLOR_BGR2GRAY)     #Convert to grayscale

    frame = cv2.resize(sourceImage, (640,480))
    
    croppedSign = localization(frame, min_size_components, similitary_contour_with_circle)

    if croppedSign is None:
        print("no signs")
    else:
        cv2.imshow('Result', croppedSign)
        signName = classify(croppedSign)
        return signName

    return classes[0]


file = cv2.imread("..\\Pictures\\HVGA\\STOP\\00016.jpg")
name = detectSign(file)

print(name)
cv2.waitKey(0)
