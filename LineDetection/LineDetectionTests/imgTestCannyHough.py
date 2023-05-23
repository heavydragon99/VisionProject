import cv2
import numpy as np

# Load the image
image = cv2.imread('C:\\VisionProject\\Pictures\\WegPlusBorden\\00016.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
cv2.imshow("edges", edges)
# Apply Hough Line Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

# Draw the detected lines on the image
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the image with the detected lines
cv2.imshow("Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
