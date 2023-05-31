import cv2
import numpy as np
import imutils

# img = cv2.imread(
#     "D:\\Github\\VisionProject\\Pictures\\HVGA\\NietAuto\\00021.jpg"
# )  # read image       max 26
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\NietInhalen\\00015.jpg")   #read image     max 19
img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\50\\00016.jpg")   #read image             max 17
# img = cv2.imread("D:\\VisionProjectPictures\\TestPictures.class\\00009(60).jpg")   #read image

# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInTeRijden\\00186.jpg")   #read image
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenStilstaan\\00380.jpg")   #read image
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenParkeren\\00220.jpg")   #read image
# template_verbodenAuto = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(200).png")
# template_verbodenInhalen = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(200).png")
# template_50 = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\50(200).png")
template_verbodenAuto = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(200).png"
)
template_verbodenInhalen = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(200).png"
)
template_50 = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\Templates\\50(200).png"
)

img = cv2.rotate(img, cv2.ROTATE_180)  # rotate (only needed for humans)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # make grayscale
gray_template_verbodenAuto = cv2.cvtColor(
    template_verbodenAuto, cv2.COLOR_BGR2GRAY
)  # make grayscale
gray_template_verbodenInhalen = cv2.cvtColor(
    template_verbodenInhalen, cv2.COLOR_BGR2GRAY
)
gray_template_50 = cv2.cvtColor(template_50, cv2.COLOR_BGR2GRAY)
blur_img = cv2.medianBlur(gray_img, 5)
canny_img = cv2.Canny(blur_img, 100, 200)

# rows = blur_img.shape[0]
circles = cv2.HoughCircles(
    canny_img,
    cv2.HOUGH_GRADIENT,
    1.3,
    10,  # cv2.HoughCircles(image, DetectionMethod, dp, minDist centers, canny high treshold, canny low treshold)
    param1=200,
    param2=75,
    minRadius=10,
    maxRadius=150,
)  # dp = 1.4 param2 = 75

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        x = i[0]
        y = i[1]
        # circle center
        cv2.circle(
            img, (x, y), 1, (0, 100, 100), 1
        )  # cv2.circle(image, center_coordinates, radius, color, thickness)
        # circle outline
        radius = i[2]
        cv2.circle(img, (x, y), radius, (255, 0, 255), 2)

    crop_img = gray_img[
        y - radius : y + radius, x - radius : x + radius
    ]  # crop image to size of detected circle

    width = 200
    height = 200
    dim = (width, height)
    resized_img = cv2.resize( crop_img, dim, interpolation=cv2.INTER_AREA)  # INTER_AREA is prob best one to use

    gray_template_verbodenAuto = imutils.rotate(gray_template_verbodenAuto, angle=339)
    gray_template_verbodenInhalen = imutils.rotate(gray_template_verbodenInhalen, angle=339)
    gray_template_50 = imutils.rotate(gray_template_50, angle=339)

    matchProcent_verbodenAuto=0
    matchProcent_verbodenInhalen=0
    matchProcent_50=0

    for x in range(-20, 21):
        gray_template_verbodenAuto = imutils.rotate(gray_template_verbodenAuto, angle=1)
        gray_template_verbodenInhalen = imutils.rotate(gray_template_verbodenInhalen, angle=1)
        gray_template_50 = imutils.rotate(gray_template_50, angle=1)

        res_verbodenAuto = cv2.matchTemplate(resized_img, gray_template_verbodenAuto, cv2.TM_CCOEFF_NORMED)
        res_verbodenInhalen = cv2.matchTemplate(resized_img, gray_template_verbodenInhalen, cv2.TM_CCOEFF_NORMED)
        res_50 = cv2.matchTemplate(resized_img, gray_template_50, cv2.TM_CCOEFF_NORMED)
        #print("Degrees are: ",-x)
        #print("match = ",res, "\n")
        #cv2.imshow(str(-x), gray_template_verbodenAuto)
        if matchProcent_verbodenAuto < res_verbodenAuto:
            matchProcent_verbodenAuto=res_verbodenAuto
        if matchProcent_verbodenInhalen < res_verbodenInhalen:
            matchProcent_verbodenInhalen=res_verbodenInhalen
        if matchProcent_50 < res_50:
            matchProcent_50=res_50
    print("procent it is template verbodenAuto: ", matchProcent_verbodenAuto)
    print("procent it is template verbodenInhalen: ", matchProcent_verbodenInhalen)
    print("procent it is template 50: ", matchProcent_50)
        
    


cv2.imshow("circle", img)
# cv2.imshow("blur", blur_img)
# cv2.imshow("canny", canny_img)
# cv2.imshow("resized", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


print("end of program")
