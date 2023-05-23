import cv2
import numpy as np

# Load the image
image = cv2.imread('C:\\VisionProject\\Pictures\\WegPlusBorden\\00016.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Apply Radon Transform
theta_range = np.linspace(0, np.pi, 180)
radon_transform = cv2.radon(edges, angles=theta_range, delta=1.0)

# Find the maximum response in the Radon space
max_response = np.max(radon_transform)

# Threshold the Radon space to extract lines
threshold = max_response * 0.7
lines = np.argwhere(radon_transform > threshold)

# Draw detected lines on the original image
for line in lines:
    angle = theta_range[line[1]]
    distance = line[0]
    a = np.cos(angle)
    b = np.sin(angle)
    x0 = a * distance
    y0 = b * distance
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Display the image with detected lines
cv2.imshow('Lines Detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
