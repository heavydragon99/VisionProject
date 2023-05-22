import cv2
import numpy as np

#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenAutos\\00290.jpg")   #read image
img = cv2.imread("D:\\VisionProjectPictures\\TestPictures.class\\00000.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInhalen\\00430.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInTeRijden\\00186.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\50\\00325.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenStilstaan\\00380.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenParkeren\\00220.jpg")   #read image
template_verbodenAuto = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(pictogram).png")
# template_verbodenInhalen = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(100).png")
# template_verbodenInRijden = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeRijden.png")
# template_50 = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\50(200).png")
# template_verbodenStilstaan = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenStilstaan(200).png")
# template_verbodenParkeren = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenParkeren(200).png")

#img = cv2.rotate(img, cv2.ROTATE_180)                                               #rotate (only needed for humans)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    #make grayscale
gray_template_verbodenAuto = cv2.cvtColor(template_verbodenAuto, cv2.COLOR_BGR2GRAY)                                    #make grayscale
#gray_template_verbodenInhalen = cv2.cvtColor(template_verbodenInhalen, cv2.COLOR_BGR2GRAY) 
# gray_template_verbodenInRijden = cv2.cvtColor(template_verbodenInRijden, cv2.COLOR_BGR2GRAY)
# gray_template_50 = cv2.cvtColor(template_50, cv2.COLOR_BGR2GRAY) 
# gray_template_verbodenStilstaan = cv2.cvtColor(template_verbodenStilstaan, cv2.COLOR_BGR2GRAY) 
# gray_template_verbodenParkeren = cv2.cvtColor(template_verbodenParkeren, cv2.COLOR_BGR2GRAY)  

# Initialize the ORB detector algorithm
orb = cv2.ORB_create()

# Detect the keypoints and compute the descriptors
keyPointsTemplate, DescriptorTemplate = orb.detectAndCompute(gray_template_verbodenAuto, None)
keyPointsPicture, DescriptorPicture = orb.detectAndCompute(gray_img, None)
# kp1, des1 = orb.detectAndCompute(resized_img,None)
# kp2, des2 = orb.detectAndCompute(gray_template_verbodenAuto,None)
# kp3, des3 = orb.detectAndCompute(gray_template_verbodenInhalen,None)
# kp4, des4 = orb.detectAndCompute(gray_template_verbodenInRijden,None)
# kp5, des5 = orb.detectAndCompute(gray_template_50,None)
# kp6, des6 = orb.detectAndCompute(gray_template_verbodenStilstaan,None)
# kp7, des7 = orb.detectAndCompute(gray_template_verbodenParkeren,None)

# Initialize the Matcher for matching
# the keypoints and then match the
# keypoints
# create BFMatcher object
matcher = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=False)
matches = matcher.match(DescriptorTemplate,DescriptorPicture)
matches = sorted(matches, key = lambda x:x.distance)

final_img = cv2.drawMatches(gray_template_verbodenAuto, keyPointsTemplate, 
gray_img, keyPointsPicture, matches[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


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

# score_VerbodenAuto = len(matchesVerbodenAuto) / len(kp2) * 100
# score_VerbodenInhalen = len(matchesVerbodenInhalen) / len(kp3) * 100
# score_VerbodenInRijden = len(matchesVerbodenInRijden) / len(kp4) * 100
# score_50 = len(matches50) / len(kp5) * 100
# score_VerbodenStilstaan = len(matchesVerbodenStilstaan) / len(kp6) * 100
# score_VerbodenParkeren = len(matchesVerbodenParkeren) / len(kp7) * 100

# print("percentage its a verbodenAuto sign")
# print(score_VerbodenAuto)

# print("percentage its a verbodenInhalen sign")
# print(score_VerbodenInhalen)

# print("percentage its a verbodenInRijden sign")
# print(score_VerbodenInRijden)

# print("percentage its a 50 sign")
# print(score_50)

# print("percentage its a verbodenStilstaan sign")
# print(score_VerbodenStilstaan)

# print("percentage its a verbodenparkeren sign")
# print(score_VerbodenParkeren)
#res = cv2.matchTemplate(resized_img,template,cv2.TM_CCOEFF)
#max = max(res)
#print(max)

# if (score_VerbodenAuto < score_VerbodenInhalen):
#     cv2.putText(img,"Inhalen",(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)        #cv2.putText(image, 'OpenCV', org, font, fontScale, color, thickness, cv2.LINE_AA)
# else:
#     cv2.putText(img,"Inrijden",(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)

# cv2.imshow('resized',resized_img)  
# cv2.imshow('detectSign',img)    
cv2.imshow("Matches", final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()





#cv2.imshow('grey_image',gray_img)
#cv2.imshow('edge detection',edges_img)
print("end of program")