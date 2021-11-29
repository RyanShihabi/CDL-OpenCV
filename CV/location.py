import cv2
import numpy as np
# import pytesseract

cap = cv2.VideoCapture('./videos/demo.mp4')

# cap.set(cv2.CAP_PROP_POS_FRAMES, 1800)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        map = frame[675:1060, 25:700]

        mblur = cv2.medianBlur(map, 3)

        gray = cv2.cvtColor(mblur, cv2.COLOR_BGR2GRAY)
        # hsl = cv2.cvtColor(map, cv2.COLOR_BGR2HLS)
        hsv = cv2.cvtColor(mblur, cv2.COLOR_BGR2HSV)

        white_lower = np.array([0, 0, 160])
        white_upper = np.array([179, 15, 255])

        mask = cv2.inRange(hsv, white_lower, white_upper)

        cv2.imshow("players", mask)

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
