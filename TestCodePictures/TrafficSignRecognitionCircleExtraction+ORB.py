import cv2
import numpy as np

#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenAutos\\00285.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInhalen\\00430.jpg")   #read image
#img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\50\\00324.jpg")   #read image
img = cv2.imread("D:\\VisionProjectPictures\\TestPictures.class\\00009(60).jpg")   #read image

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
blur_img = cv2.medianBlur(gray_img, 9)

rows = blur_img.shape[0]
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

    crop_img = gray_img[y-radius:y+radius, x-radius:x+radius]      #crop image to size of detected circle  

    width = 200
    height = 200
    dim = (width, height )
    resized_img = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA     )

    orb = cv2.ORB_create()
    keyPointsPicture, DescriptorPicture = orb.detectAndCompute(resized_img, None)
    keyPointsTemplate_verbodenAuto, DescriptorTemplate_verbodenAuto = orb.detectAndCompute(gray_template_verbodenAuto, None)    
    keyPointsTemplate_verbodenInhalen, DescriptorTemplate_verbodenInhalen = orb.detectAndCompute(gray_template_verbodenInhalen,None)
    keyPointsTemplate_50, DescriptorTemplate_50 = orb.detectAndCompute(gray_template_50,None)
    

    # create BFMatcher object
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2,crossCheck=True)

    matches_verbodenAuto        = matcher.match(DescriptorTemplate_verbodenAuto,DescriptorPicture)
    matches_verbodenInhalen     = matcher.match(DescriptorTemplate_verbodenInhalen,DescriptorPicture)
    matches_50                  = matcher.match(DescriptorTemplate_50,DescriptorPicture)
   
    final_img1 = cv2.drawMatches(gray_template_verbodenAuto, keyPointsTemplate_verbodenAuto,
    resized_img, keyPointsPicture, matches_verbodenAuto[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img2 = cv2.drawMatches(gray_template_verbodenInhalen, keyPointsTemplate_verbodenInhalen,
    resized_img, keyPointsPicture, matches_verbodenInhalen[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    final_img4 = cv2.drawMatches(gray_template_50, keyPointsTemplate_50,
    resized_img, keyPointsPicture, matches_50[:50],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    

    score_VerbodenAuto = len(matches_verbodenAuto) / len(keyPointsTemplate_verbodenAuto) * 100
    score_VerbodenInhalen = len(matches_verbodenInhalen) / len(keyPointsTemplate_verbodenInhalen) * 100
    score_50 = len(matches_50) / len(keyPointsTemplate_50) * 100

    print("percentage its a verbodenAuto sign")
    print(score_VerbodenAuto)

    print("percentage its a verbodenInhalen sign")
    print(score_VerbodenInhalen)

    print("percentage its a 50 sign")
    print(score_50)

    cv2.imshow('final1',final_img1)
    cv2.imshow('final2',final_img2)   
    cv2.imshow('final4',final_img4)       
    cv2.waitKey(0)
    cv2.destroyAllWindows()


print("end of program")