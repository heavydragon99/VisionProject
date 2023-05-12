import cv2
import numpy as np

# Load image
img = cv2.imread('C:\\VisionProject\\Pictures\\WegPlusBorden\\00000.jpg')
img = cv2.rotate(img, cv2.ROTATE_180)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('img', gray_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
