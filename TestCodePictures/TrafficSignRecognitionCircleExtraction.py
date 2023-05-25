# import cv2
# import numpy as np

# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenAutos\\00280.jpg")   #read image
# #img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInhalen\\00430.jpg")   #read image
# #img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInTeRijden\\00186.jpg")   #read image
# #img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\50\\00325.jpg")   #read image
# #img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenStilstaan\\00380.jpg")   #read image
# #img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenParkeren\\00220.jpg")   #read image
# template_verbodenAuto = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(100).png")
# template_verbodenInhalen = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(100).png")
# template_verbodenInRijden = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeRijden.png")
# template_50 = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\50(200).png")
# template_verbodenStilstaan = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenStilstaan(200).png")
# template_verbodenParkeren = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenParkeren(200).png")

# img = cv2.rotate(img, cv2.ROTATE_180)                                               #rotate (only needed for humans)
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    #make grayscale
# gray_template_verbodenAuto = cv2.cvtColor(template_verbodenAuto, cv2.COLOR_BGR2GRAY)                                    #make grayscale
# gray_template_verbodenInhalen = cv2.cvtColor(template_verbodenInhalen, cv2.COLOR_BGR2GRAY) 
# gray_template_verbodenInRijden = cv2.cvtColor(template_verbodenInRijden, cv2.COLOR_BGR2GRAY)
# gray_template_50 = cv2.cvtColor(template_50, cv2.COLOR_BGR2GRAY) 
# gray_template_verbodenStilstaan = cv2.cvtColor(template_verbodenStilstaan, cv2.COLOR_BGR2GRAY) 
# gray_template_verbodenParkeren = cv2.cvtColor(template_verbodenParkeren, cv2.COLOR_BGR2GRAY)  
# blur_img = cv2.medianBlur(gray_img, 3)
# edges_img = cv2.Canny(gray_img,100,200)                                             #edge detection with canny

# rows = blur_img.shape[0]
# circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, rows/8,                      #cv2.HoughCircles(image, DetectionMethod, dp, minDist centers, canny high treshold, canny low treshold)
#                                param1=200, param2=30,
#                                minRadius=1, maxRadius=30)

# if circles is not None:
#     circles = np.uint16(np.around(circles))
#     for i in circles[0, :]:
#         x = i[0]
#         y = i[1]
#         # circle center
#         cv2.circle(img, (x,y), 1, (0, 100, 100), 1)            #cv2.circle(image, center_coordinates, radius, color, thickness)
#         # circle outline
#         radius = i[2]
#         cv2.circle(img, (x,y), radius, (255, 0, 255), 2)

#     crop_img = gray_img[y-radius:y+radius, x-radius:x+radius]      #crop image to size of detected circle  

#     width = 200
#     height = 200
#     dim = (width, height )
#     resized_img = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)

#     orb = cv2.ORB_create()
#     kp1, des1 = orb.detectAndCompute(resized_img,None)
#     kp2, des2 = orb.detectAndCompute(gray_template_verbodenAuto,None)
#     kp3, des3 = orb.detectAndCompute(gray_template_verbodenInhalen,None)
#     kp4, des4 = orb.detectAndCompute(gray_template_verbodenInRijden,None)
#     kp5, des5 = orb.detectAndCompute(gray_template_50,None)
#     kp6, des6 = orb.detectAndCompute(gray_template_verbodenStilstaan,None)
#     kp7, des7 = orb.detectAndCompute(gray_template_verbodenParkeren,None)
    

#     # create BFMatcher object
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     # Match descriptors.
#     matchesVerbodenAuto = bf.match(des2,des1)
#     matchesVerbodenInhalen = bf.match(des3,des1)
#     matchesVerbodenInRijden = bf.match(des4,des1)
#     matches50 = bf.match(des5,des1)
#     matchesVerbodenStilstaan = bf.match(des6,des1)
#     matchesVerbodenParkeren = bf.match(des7,des1)
#     # Sort them in the order of their distance.
#     #matches = sorted(matches, key = lambda x:x.distance)

#     # Draw first 10 matches.
#     #img3 = cv2.drawMatches(gray_template,kp1,resized_img,kp2,matches[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#     score_VerbodenAuto = len(matchesVerbodenAuto) / len(kp2) * 100
#     score_VerbodenInhalen = len(matchesVerbodenInhalen) / len(kp3) * 100
#     score_VerbodenInRijden = len(matchesVerbodenInRijden) / len(kp4) * 100
#     score_50 = len(matches50) / len(kp5) * 100
#     score_VerbodenStilstaan = len(matchesVerbodenStilstaan) / len(kp6) * 100
#     score_VerbodenParkeren = len(matchesVerbodenParkeren) / len(kp7) * 100

#     print("percentage its a verbodenAuto sign")
#     print(score_VerbodenAuto)

#     print("percentage its a verbodenInhalen sign")
#     print(score_VerbodenInhalen)

#     print("percentage its a verbodenInRijden sign")
#     print(score_VerbodenInRijden)

#     print("percentage its a 50 sign")
#     print(score_50)

#     print("percentage its a verbodenStilstaan sign")
#     print(score_VerbodenStilstaan)

#     print("percentage its a verbodenparkeren sign")
#     print(score_VerbodenParkeren)
#     #res = cv2.matchTemplate(resized_img,template,cv2.TM_CCOEFF)
#     #max = max(res)
#     #print(max)

#     # if (score_VerbodenAuto < score_VerbodenInhalen):
#     #     cv2.putText(img,"Inhalen",(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)        #cv2.putText(image, 'OpenCV', org, font, fontScale, color, thickness, cv2.LINE_AA)
#     # else:
#     #     cv2.putText(img,"Inrijden",(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)

#     cv2.imshow('resized',resized_img)  
#     cv2.imshow('detectSign',img)    
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()





# #cv2.imshow('grey_image',gray_img)
# #cv2.imshow('edge detection',edges_img)
# print("end of program")

import cv2
import numpy as np

img = cv2.imread("C:\\Users\\siemv\\OneDrive\\Documenten\\GitHub\\VisionProject\\Pictures\\HVGA\\StoplichtGroen\\00016.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInhalen\\00430.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInTeRijden\\00186.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\50\\00325.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenStilstaan\\00380.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenParkeren\\00220.jpg")   #read image
template_verbodenAuto = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(100).png")
template_verbodenInhalen = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(100).png")
template_verbodenInRijden = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeRijden.png")
template_50 = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\50(100).png")
template_verbodenStilstaan = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenStilstaan.png")
template_verbodenParkeren = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenParkeren.png")

img = cv2.rotate(img, cv2.ROTATE_180)                                               #rotate (only needed for humans)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    #make grayscale
gray_template_verbodenAuto = cv2.cvtColor(template_verbodenAuto, cv2.COLOR_BGR2GRAY)                                    #make grayscale
gray_template_verbodenInhalen = cv2.cvtColor(template_verbodenInhalen, cv2.COLOR_BGR2GRAY) 
gray_template_verbodenInRijden = cv2.cvtColor(template_verbodenInRijden, cv2.COLOR_BGR2GRAY)
gray_template_50 = cv2.cvtColor(template_50, cv2.COLOR_BGR2GRAY) 
gray_template_verbodenStilstaan = cv2.cvtColor(template_verbodenStilstaan, cv2.COLOR_BGR2GRAY) 
gray_template_verbodenParkeren = cv2.cvtColor(template_verbodenParkeren, cv2.COLOR_BGR2GRAY)  
blur_img = cv2.medianBlur(gray_img, 3)
edges_img = cv2.Canny(gray_img,100,200)                                             #edge detection with canny

rows = blur_img.shape[0]
circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, rows/8,                      #cv2.HoughCircles(image, DetectionMethod, dp, minDist centers, canny high treshold, canny low treshold)
                               param1=200, param2=30,
                               minRadius=1, maxRadius=30)

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

    crop_img = gray_img[y-radius:y+radius, x-radius:x+radius]      #crop image to size of detected circle  

    width = 200
    height = 200
    dim = (width, height )
    resized_img = cv2.resize(crop_img, dim, interpolation = cv2.INTER_CUBIC     )

    orb = cv2.ORB_create()
    keyPointsPicture, DescriptorPicture = orb.detectAndCompute(resized_img, None)
    keyPointsTemplate_verbodenAuto, DescriptorTemplate_verbodenAuto = orb.detectAndCompute(gray_template_verbodenAuto, None)    
    keyPointsTemplate_verbodenInhalen, DescriptorTemplate_verbodenInhalen = orb.detectAndCompute(gray_template_verbodenInhalen,None)
    keyPointsTemplate_verbodenInRijden, DescriptorTemplate_verbodenInRijden = orb.detectAndCompute(gray_template_verbodenInRijden,None)
    keyPointsTemplate_50, DescriptorTemplate_50 = orb.detectAndCompute(gray_template_50,None)
    keyPointsTemplate_verbodenStilstaan, DescriptorTemplate_verbodenStilstaan = orb.detectAndCompute(gray_template_verbodenStilstaan,None)
    keyPointsTemplate_verbodenParkeren, DescriptorTemplate_verbodenParkeren = orb.detectAndCompute(gray_template_verbodenParkeren,None)
    

    # create BFMatcher object
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2,crossCheck=True)

    matches_verbodenAuto        = matcher.match(DescriptorTemplate_verbodenAuto,DescriptorPicture)
    matches_verbodenInhalen     = matcher.match(DescriptorTemplate_verbodenInhalen,DescriptorPicture)
    matches_verbodenInRijden    = matcher.match(DescriptorTemplate_verbodenInRijden,DescriptorPicture)
    matches_50                  = matcher.match(DescriptorTemplate_50,DescriptorPicture)
    matches_verbodenStilstaan   = matcher.match(DescriptorTemplate_verbodenStilstaan,DescriptorPicture)
    matches_verbodenParkeren    = matcher.match(DescriptorTemplate_verbodenParkeren,DescriptorPicture)
   
    final_img1 = cv2.drawMatches(gray_template_verbodenAuto, keyPointsTemplate_verbodenAuto,
    resized_img, keyPointsPicture, matches_verbodenAuto[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img2 = cv2.drawMatches(gray_template_verbodenInhalen, keyPointsTemplate_verbodenInhalen,
    resized_img, keyPointsPicture, matches_verbodenInhalen[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img3 = cv2.drawMatches(gray_template_verbodenInRijden, keyPointsTemplate_verbodenInRijden,
    resized_img, keyPointsPicture, matches_verbodenInRijden[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img4 = cv2.drawMatches(gray_template_50, keyPointsTemplate_50,
    resized_img, keyPointsPicture, matches_50[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img5 = cv2.drawMatches(gray_template_verbodenStilstaan, keyPointsTemplate_verbodenStilstaan,
    resized_img, keyPointsPicture, matches_verbodenStilstaan[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img6 = cv2.drawMatches(gray_template_verbodenParkeren, keyPointsTemplate_verbodenParkeren,
    resized_img, keyPointsPicture, matches_verbodenParkeren[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    

    score_VerbodenAuto = len(matches_verbodenAuto) / len(keyPointsTemplate_verbodenAuto) * 100
    score_VerbodenInhalen = len(matches_verbodenInhalen) / len(keyPointsTemplate_verbodenInhalen) * 100
    score_VerbodenInRijden = len(matches_verbodenInRijden) / len(keyPointsTemplate_verbodenInRijden) * 100
    score_50 = len(matches_50) / len(keyPointsTemplate_50) * 100
    score_VerbodenStilstaan = len(matches_verbodenStilstaan) / len(keyPointsTemplate_verbodenStilstaan) * 100
    score_VerbodenParkeren = len(matches_verbodenParkeren) / len(keyPointsTemplate_verbodenParkeren) * 100

    print("percentage its a verbodenAuto sign")
    print(score_VerbodenAuto)

    print("percentage its a verbodenInhalen sign")
    print(score_VerbodenInhalen)

    print("percentage its a verbodenInRijden sign")
    print(score_VerbodenInRijden)

    print("percentage its a 50 sign")
    print(score_50)

    print("percentage its a verbodenStilstaan sign")
    print(score_VerbodenStilstaan)

    print("percentage its a verbodenparkeren sign")
    print(score_VerbodenParkeren)

    cv2.imshow('final1',final_img1)
    cv2.imshow('final2',final_img2)   
    #cv2.imshow('final3',final_img3)   
    cv2.imshow('final4',final_img4)   
    cv2.imshow('final5',final_img5)   
    cv2.imshow('final6',final_img6)      
    cv2.waitKey(0)
    cv2.destroyAllWindows()


print("end of program")