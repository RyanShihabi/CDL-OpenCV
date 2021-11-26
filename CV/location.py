import cv2
import numpy as np

cap = cv2.VideoCapture('./videos/demo.mp4')

cap.set(cv2.CAP_PROP_POS_FRAMES, 2400)

while cap.isOpened():
    ret, frame = cap.read()

    frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    if ret:
        map = frame[675:1050, 25:700]
        # cv2.imshow("none", map)

        mblur = cv2.medianBlur(map, 3)
        # gblur = cv2.GaussianBlur(mblur, (3,3), 0)

        gray = cv2.cvtColor(mblur, cv2.COLOR_BGR2GRAY)
        # hsl = cv2.cvtColor(map, cv2.COLOR_BGR2HLS)

        # cv2.imshow("hsl", hsl)

        # lower_gray = np.array([140, 140, 140])
        # upper_gray = np.array([170, 170, 170])
        # # Threshold the HSV image to get only blue colors
        # mask = cv2.inRange(map, lower_gray, upper_gray)
        # # Bitwise-AND mask and original image
        # res = cv2.bitwise_and(map, map, mask=mask)

        # cv2.imshow("gray", res)

        mid = cv2.Canny(gray, 30, 100, L2gradient=True)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph = cv2.morphologyEx(mid, cv2.MORPH_GRADIENT, kernel)

        # cv2.imshow("mcanny", morph)

        contours, hierarchy = cv2.findContours(image=morph, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        # if len(contours) > 0:
        #     cv2.drawContours(map, contours, -1, (0, 255, 0), 5)
        #     c = max(contours, key=cv2.contourArea)
        #     x,y,w,h = cv2.boundingRect(c)
        #
        #     cv2.rectangle(map, (x,y), (x+w, y+h), (0, 0, 255), 8)

        cv2.rectangle(frame, (35, 725), (445, 1040), (0, 0, 255), 3)

        # RAID1080: [(30, 725), (450, 1045)]

        cv2.imshow("map", map)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
