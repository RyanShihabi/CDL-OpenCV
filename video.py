from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# try reading the entire screen
frame_count = 24000

cap = cv2.VideoCapture("videos/Winners Round 2 _ @Dallas Empire vs @Toronto Ultra _ Championship Weekend _ Day 2-OTsYiHhrDPw.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 24000)

while cap.isOpened():
# while fvs.more():
    # frame = fvs.read()
    ret, frame = cap.read()

    cv2.imshow("Frame", frame)
    print(frame_count)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
fvs.stop()
