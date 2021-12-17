import cv2
import numpy as np

cap = cv2.VideoCapture('./videos/demo.mp4')

# cap.set(cv2.CAP_PROP_POS_FRAMES, 1800)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        map = frame[675:1060, 25:700]

        focus = frame[725:1040, 35:445]

        # cv2.imshow("focused", focus)

        mblur = cv2.medianBlur(map, 3)
        fblur = cv2.medianBlur(focus, 3)

        gray = cv2.cvtColor(mblur, cv2.COLOR_BGR2GRAY)

        # cv2.imshow("gray", gray)

        hsv = cv2.cvtColor(fblur, cv2.COLOR_BGR2HSV)

        white_lower = np.array([0, 0, 169])
        white_upper = np.array([255, 255, 255])

        mask = cv2.inRange(hsv, white_lower, white_upper)

        kernel_player = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph_player = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_player)

        cv2.imshow("players", morph_player)

        mid = cv2.Canny(gray, 30, 100, L2gradient=True)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph = cv2.morphologyEx(mid, cv2.MORPH_GRADIENT, kernel)

        cv2.imshow("mcanny", morph)

        contours, hierarchy = cv2.findContours(image=morph, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        cv2.rectangle(frame, (35, 725), (445, 1040), (0, 0, 255), 3)

        cv2.imshow("map", map)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
