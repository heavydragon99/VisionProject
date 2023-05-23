import cv2
import numpy as np

# Load the image
image = cv2.imread('C:\\VisionProject\\Pictures\\WegPlusBorden\\00038.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create an LSD detector object
lsd = cv2.createLineSegmentDetector()

# Detect line segments in the image
lines, width, prec, nfa = lsd.detect(gray)

# Draw the detected lines on the image
image_with_lines = lsd.drawSegments(image, lines)

# Display the image with the detected lines
cv2.imshow("Lines", image_with_lines)
cv2.waitKey(0)
cv2.destroyAllWindows()
