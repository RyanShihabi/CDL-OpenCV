import cv2
import os
import argparse
from imutils.video import FPS
from grab import *

ap = ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="input VOD for clip detection")
ap.add_argument("-l", "--link", required=True, help="input youtube URL")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])
fps = FPS().start()

while video.isOpened():
    ret, frame = video.read()
    cv2.imshow('VOD', frame)

    # print(frame)
    map = grabMap(frame)

    #figure out a way to store the map for the time being
        # map should be different from the one before it
        # Add a check map loop
        # once video is over, clear map history

    if map != "":
        grabFeed(frame, int(fps.elapsed()))

    fps.update()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fps.stop()
video.release()
cv2.destroyAllWindows()
