import cv2
import os
import argparse
from imutils.video import FPS
from grab import *

ap = ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="input VOD for clip detection")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])
fps = FPS().start()

while True:
    ret, frame = video.read()
    cv2.imshow('VOD', frame)

    # print(frame)
    map = grabMap(frame)

    if map != "":
        grabFeed(frame, int(fps.elapsed()))

    fps.update()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fps.stop()
video.release()
cv2.destroyAllWindows()
