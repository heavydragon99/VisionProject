import cv2
import numpy as np

def readImage(imgpath,rotateValue):
    img = cv2.imread(imgpath)
    img = cv2.rotate(img, rotateValue)
    return img

# Load image
image = readImage('C:\\VisionProject\\Pictures\\WegPlusBorden\\00017.jpg',cv2.ROTATE_180)
# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through contours and fit lines
for contour in contours:
    # Ignore small contours
    if cv2.contourArea(contour) > 100:
        # Fit a line to the contour
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        # Calculate the start and end points of the line
        lefty = int((-x * vy / vx) + y)
        righty = int(((gray.shape[1] - x) * vy / vx) + y)
        # Draw the line
        cv2.line(image, (gray.shape[1] - 1, righty), (0, lefty), (0, 0, 255), 2)

# Display the result
cv2.imshow('Line Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
