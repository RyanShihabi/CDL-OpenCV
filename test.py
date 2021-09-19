from PIL import Image
import pytesseract
import argparse
import numpy
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="input image path for OCR")
ap.add_argument("-d", "--detection", help="choose text to detect")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

# roi = image[350:475, 0:125]
#

print((image.shape[1], image.shape[0]))

# try resizing the image to get broader pixel values
# You only need to look on the left side of the kill feed. That determines a clip
# Map text detection works best with blur filter
# Kill feed text detects best with blur filter
# figure out if there are better blur methods
# maybe start using masking to filter out unwanted COLOR
# test kill feed on multiple scenarios
    # five players on feed

if args["detection"] == "map":
    #720p roi
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # map_roi = gray[585:640, 240:550]

    #1080
    map_roi = gray[875:975, 345:900]

    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename, map_roi)
    cv2.imshow("Output", map_roi)

if args["detection"] == "feed":
    #720p roi
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    feed_roi = image[300:475, 0:275]

    feed_roi = cv2.medianBlur(feed_roi, 1)

    width = int(feed_roi.shape[1] * 300 / 100)
    height = int(feed_roi.shape[0] * 300 / 100)

    feed_roi = cv2.resize(feed_roi, (width, height), interpolation = cv2.INTER_AREA)

    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename, feed_roaptivecv2._THREi   )
np. thersh   cv2.imshow("Output", feed_roi)

text = pytesseract.image_to_string(Image.open(filename), lang="eng", config="--psm 6 --oem 1")
os.remove(filename)
print(text)

# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
cv2.waitKey(0)

if args["detection"] == "map":
    text = text.split("-")[0]
if args["detection"] == "feed":
    text = text.split('\n')[:-1]
    # players format [['clan tag', 'gamertag'], ...]
    players = []
    for line in text:
        if line[0] in ['[', '(']:
            players.append(line.split(" ")[:2])

    print(players)
    # print(isClip(players))
    # print(isClip([['[ATL]', 'gamertag'], ['(Atl]', 'gamertag']]))
