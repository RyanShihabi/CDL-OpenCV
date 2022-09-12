import numpy as np
import argparse
import time
import cv2

cap = cv2.VideoCapture("videos/count.mp4")

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        cv2.imshow("Frame", frame)
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("done")
