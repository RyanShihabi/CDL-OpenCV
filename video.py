import cv2
import os
import argparse
from grab import *

ap = ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="input VOD for clip detection")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])

while True:
    ret, frame = video.read()

    cv2.imshow('VOD', frame)

    grabFeed(frame)
    grabMap(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()

cv2.destroyAllWindows()
