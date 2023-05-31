import cv2
import numpy as np

img = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\HVGA\\NietAuto\\00026.jpg"
)  # read image       max 26
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\NietInhalen\\00019.jpg")   #read image     max 19
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\HVGA\\50\\00017.jpg")   #read image             max 17
# img = cv2.imread("D:\\VisionProjectPictures\\TestPictures.class\\00009(60).jpg")   #read image

# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenInTeRijden\\00186.jpg")   #read image
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenStilstaan\\00380.jpg")   #read image
# img = cv2.imread("D:\\Github\\VisionProject\\Pictures\\VerbodenParkeren\\00220.jpg")   #read image
# template_verbodenAuto = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenAutos(200).png")
# template_verbodenInhalen = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\VerbodenInTeHalen(200).png")
# template_50 = cv2.imread("D:\\Github\\VisionProject\\Pictures\\Templates\\50(200).png")
template_verbodenAuto = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\RealLifeTemplates\\NietAuto.jpg"
)
template_verbodenInhalen = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\RealLifeTemplates\\NietInhalen.jpg"
)
template_50 = cv2.imread(
    "D:\\Github\\VisionProject\\Pictures\\RealLifeTemplates\\50.jpg"
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
    2,
    10,  # cv2.HoughCircles(image, DetectionMethod, dp, minDist centers, canny high treshold, canny low treshold)
    param1=200,
    param2=100,
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

    width = 175
    height = 175
    dim = (width, height)
    resized_img = cv2.resize(
        crop_img, dim, interpolation=cv2.INTER_AREA
    )  # INTER_AREA is prob best one to use

    orb = cv2.ORB_create()
    keyPointsPicture, DescriptorPicture = orb.detectAndCompute(resized_img, None)
    (
        keyPointsTemplate_verbodenAuto,
        DescriptorTemplate_verbodenAuto,
    ) = orb.detectAndCompute(gray_template_verbodenAuto, None)
    (
        keyPointsTemplate_verbodenInhalen,
        DescriptorTemplate_verbodenInhalen,
    ) = orb.detectAndCompute(gray_template_verbodenInhalen, None)
    keyPointsTemplate_50, DescriptorTemplate_50 = orb.detectAndCompute(
        gray_template_50, None
    )

    # create BFMatcher object
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)

    matches_verbodenAuto = matcher.match(
        DescriptorTemplate_verbodenAuto, DescriptorPicture
    )
    matches_verbodenInhalen = matcher.match(
        DescriptorTemplate_verbodenInhalen, DescriptorPicture
    )
    matches_50 = matcher.match(DescriptorTemplate_50, DescriptorPicture)

    final_img1 = cv2.drawMatches(
        gray_template_verbodenAuto,
        keyPointsTemplate_verbodenAuto,
        resized_img,
        keyPointsPicture,
        matches_verbodenAuto[:20],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    final_img2 = cv2.drawMatches(
        gray_template_verbodenInhalen,
        keyPointsTemplate_verbodenInhalen,
        resized_img,
        keyPointsPicture,
        matches_verbodenInhalen[:20],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    final_img4 = cv2.drawMatches(
        gray_template_50,
        keyPointsTemplate_50,
        resized_img,
        keyPointsPicture,
        matches_50[:20],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    score_VerbodenAuto = (
        len(matches_verbodenAuto) / len(keyPointsTemplate_verbodenAuto) * 100
    )
    score_VerbodenInhalen = (
        len(matches_verbodenInhalen) / len(keyPointsTemplate_verbodenInhalen) * 100
    )
    score_50 = len(matches_50) / len(keyPointsTemplate_50) * 100

    #         # FLANN Matcher
    # index_params = dict(algorithm=cv2.FLANN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)  # or pass an empty dictionary for the default parameters
    # flann = cv2.FlannBasedMatcher(index_params, search_params)

    # matches_verbodenAuto = flann.knnMatch(DescriptorTemplate_verbodenAuto, DescriptorPicture, k=2)
    # matches_verbodenInhalen = flann.knnMatch(DescriptorTemplate_verbodenInhalen, DescriptorPicture, k=2)
    # matches_50 = flann.knnMatch(DescriptorTemplate_50, DescriptorPicture, k=2)

    # # Apply ratio test to filter good matches
    # good_matches_verbodenAuto = []
    # for m, n in matches_verbodenAuto:
    #     if m.distance < 0.7 * n.distance:  # You can adjust the ratio threshold as needed
    #         good_matches_verbodenAuto.append(m)

    # # Apply ratio test to filter good matches
    # good_matches_verbodenInhalen = []
    # for m, n in matches_verbodenInhalen:
    #     if m.distance < 0.7 * n.distance:  # You can adjust the ratio threshold as needed
    #         good_matches_verbodenInhalen.append(m)

    # # Apply ratio test to filter good matches
    # good_matches_50 = []
    # for m, n in matches_50:
    #     if m.distance < 0.7 * n.distance:  # You can adjust the ratio threshold as needed
    #         good_matches_50.append(m)

    # score_VerbodenAuto = len(good_matches_verbodenAuto) / len(keyPointsTemplate_verbodenAuto) * 100
    # score_VerbodenInhalen = len(good_matches_verbodenInhalen) / len(keyPointsTemplate_verbodenInhalen) * 100
    # score_50 = len(good_matches_50) / len(keyPointsTemplate_50) * 100

    # # Draw matches
    # final_img1 = cv2.drawMatches(gray_template_verbodenAuto, keyPointsTemplate_verbodenAuto, resized_img, keyPointsPicture,
    #                             good_matches_verbodenAuto[:20], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # # Draw matches
    # final_img2 = cv2.drawMatches(gray_template_verbodenInhalen, keyPointsTemplate_verbodenInhalen, resized_img, keyPointsPicture,
    #                             good_matches_verbodenInhalen[:20], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # # Draw matches
    # final_img4 = cv2.drawMatches(gray_template_50, keyPointsTemplate_50, resized_img, keyPointsPicture,
    #                             good_matches_50[:20], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    print("percentage its a verbodenAuto sign")
    print(round(score_VerbodenAuto))

    print("percentage its a verbodenInhalen sign")
    print(round(score_VerbodenInhalen))

    print("percentage its a 50 sign")
    print(round(score_50))

    cv2.imshow("circle", img)
    cv2.imshow("final1", final_img1)
    cv2.imshow("final2", final_img2)
    cv2.imshow("final4", final_img4)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cv2.imshow("circle", img)
cv2.imshow("blur", blur_img)
cv2.imshow("canny", canny_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


print("end of program")
