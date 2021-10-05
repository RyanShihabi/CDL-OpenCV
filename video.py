from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# try reading the entire screen

cap = cv2.VideoCapture("videos/FazeTorontoRaid.mp4")

fvs = FileVideoStream("videos/FazeTorontoRaid.mp4").start()
time.sleep(1.0)
# start the FPS timer
fps = FPS().start()

while cap.isOpened():
# while fvs.more():
    # frame = fvs.read()
    ret, frame = cap.read()

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()
fvs.stop()
