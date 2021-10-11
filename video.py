from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# try reading the entire screen
# frame_count = 24000

cap = cv2.VideoCapture("videos/count.mp4")

while cap.isOpened():
# while fvs.more():
    # frame = fvs.read()
    ret, frame = cap.read()

    # cv2.imshow("Frame", frame)
    # print(frame_count)

    # frame_count += 1

    if ret:
        cv2.imshow("Frame", frame)
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("done")
