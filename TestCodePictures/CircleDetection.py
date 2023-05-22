import cv2
import numpy as np

img = cv2.imread("D:\\VisionProjectPictures\\TestPictures.class\\00009.jpg")   #read image
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    #make grayscale
blur_img = cv2.medianBlur(gray_img, 9)
rows = blur_img.shape[0]
edges_img = cv2.Canny(gray_img,50,200)                                             #edge detection with canny
circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, rows/8,                      #cv2.HoughCircles(image, DetectionMethod, dp, minDist centers, canny high treshold, canny low treshold)
                               param1=200, param2=50,
                               minRadius=20, maxRadius=100)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        x = i[0]
        y = i[1]
        # circle center
        cv2.circle(img, (x,y), 1, (0, 100, 100), 1)            #cv2.circle(image, center_coordinates, radius, color, thickness)
        # circle outline
        radius = i[2]
        cv2.circle(img, (x,y), radius, (255, 0, 255), 2)

cv2.imshow('final',img)       
cv2.waitKey(0)
cv2.destroyAllWindows()