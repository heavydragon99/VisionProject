import cv2
import numpy as np

img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\NietAuto\\00025.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\NietInhalen\\00000.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\50\\00000.jpg")   #read image
#img = cv2.imread("D:\\VisionProjectPictures\\TestPictures.class\\00009(60).jpg")   #read image

#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInTeRijden\\00186.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenStilstaan\\00380.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenParkeren\\00220.jpg")   #read image
template_verbodenAuto = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(200).png")
template_verbodenInhalen = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(200).png")
template_50 = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\50(200).png")

img = cv2.rotate(img, cv2.ROTATE_180)                                               #rotate (only needed for humans)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    #make grayscale
gray_template_verbodenAuto = cv2.cvtColor(template_verbodenAuto, cv2.COLOR_BGR2GRAY)                                    #make grayscale
gray_template_verbodenInhalen = cv2.cvtColor(template_verbodenInhalen, cv2.COLOR_BGR2GRAY) 
gray_template_50 = cv2.cvtColor(template_50, cv2.COLOR_BGR2GRAY) 

# Initialize the ORB detector algorithm
orb = cv2.ORB_create()

# Detect the keypoints and compute the descriptors
keyPointsPicture, DescriptorPicture = orb.detectAndCompute(gray_img, None)
keyPointsTemplate_verbodenAuto, DescriptorTemplate_verbodenAuto = orb.detectAndCompute(gray_template_verbodenAuto, None)    
keyPointsTemplate_verbodenInhalen, DescriptorTemplate_verbodenInhalen = orb.detectAndCompute(gray_template_verbodenInhalen,None)
keyPointsTemplate_50, DescriptorTemplate_50 = orb.detectAndCompute(gray_template_50,None)

# Initialize the Matcher for matching
# the keypoints and then match the
# keypoints
# create BFMatcher object
matcher = cv2.BFMatcher(cv2.NORM_HAMMING2,crossCheck=True)
matches_verbodenAuto        = matcher.match(DescriptorTemplate_verbodenAuto,DescriptorPicture)
matches_verbodenInhalen     = matcher.match(DescriptorTemplate_verbodenInhalen,DescriptorPicture)
matches_50                  = matcher.match(DescriptorTemplate_50,DescriptorPicture)
matches_verbodenAuto = sorted(matches_verbodenAuto, key = lambda x:x.distance)
matches_verbodenInhalen = sorted(matches_verbodenInhalen, key = lambda x:x.distance)
matches_50 = sorted(matches_50, key = lambda x:x.distance)

final_img1 = cv2.drawMatches(gray_template_verbodenAuto, keyPointsTemplate_verbodenAuto, 
gray_img, keyPointsPicture, matches_verbodenAuto[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

final_img2 = cv2.drawMatches(gray_template_verbodenInhalen, keyPointsTemplate_verbodenInhalen, 
gray_img, keyPointsPicture, matches_verbodenInhalen[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

final_img3 = cv2.drawMatches(gray_template_50, keyPointsTemplate_50, 
gray_img, keyPointsPicture, matches_50[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


# create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# Match descriptors.
# matchesVerbodenAuto = bf.match(des2,des1)
# matchesVerbodenInhalen = bf.match(des3,des1)
# matchesVerbodenInRijden = bf.match(des4,des1)
# matches50 = bf.match(des5,des1)
# matchesVerbodenStilstaan = bf.match(des6,des1)
# matchesVerbodenParkeren = bf.match(des7,des1)
# Sort them in the order of their distance.
#matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
#img3 = cv2.drawMatches(gray_template,kp1,resized_img,kp2,matches[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imshow("Final1", final_img1)
cv2.imshow("Final2", final_img2)
cv2.imshow("Final3", final_img3)
cv2.waitKey(0)
cv2.destroyAllWindows()





#cv2.imshow('grey_image',gray_img)
#cv2.imshow('edge detection',edges_img)
print("end of program")