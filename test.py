from PIL import Image
import pytesseract
import argparse
import numpy as np
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
    cv2.imwrite(filename, feed_roi)
    cv2.imshow("Output", feed_roi)

if args["detection"] == "timer":
    feed_roi = image[445:725, 550:1400]

    feed_roi = cv2.threshold(np.array(feed_roi), 125, 255, cv2.THRESH_BINARY)[1]

    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename, feed_roi)
    cv2.imshow("Output", feed_roi)

if args["detection"] == "color":
    colors = []

    team1_roi = image[25:60, 300:350]
    team1 = [team1_roi[0, 0], team1_roi[34, 49]]

    if (team1[0][0] >= 255-55) and (team1[0][1] >= 255-55) and (team1[0][2] >= 255-55):
        colors.append({"bounds": team1, "color_space": "HLS"})
    else:
        colors.append({"bounds": team1, "color_space": "BGR"})

    team2_roi = image[25:60, 1550:1600]
    team2 = [team2_roi[0, 0], team2_roi[34, 49]]

    if (team2[0][0] >= 255-55) and (team2[0][1] >= 255-55) and (team2[0][2] >= 255-55):
        colors.append({"bounds": team2, "color_space": "HLS"})
    else:
        colors.append({"bounds": team2, "color_space": "BGR"})

    print(colors)
    print(colors[0]["bounds"][0])

    cv2.imshow("team1", team1_roi)

    cv2.imshow("team2", team2_roi)

    cv2.waitKey(0)

if args["detection"] == "game":
    roi = image[150:200, 900:1050]
    width = int(roi.shape[1] * 250 / 100)
    height = int(roi.shape[0] * 250 / 100)

    roi = cv2.resize(roi, (width, height), interpolation = cv2.INTER_AREA)
    roi = cv2.medianBlur(roi, 3)

    roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]
    filename = f"{os.getpid()}.png"

    cv2.imwrite(filename, roi)
    cv2.imshow("game", roi)

text = pytesseract.image_to_string(Image.open(filename), lang="eng", config="--psm 6 --oem 1")
os.remove(filename)
print(text)

cv2.waitKey(0)

if args["detection"] == "game":
    modes = ["CONTROL", "HARDPOINT", "SEARCH & DESTROY"]

    text = text.split("\n")[0]

    if text in modes:
        print("In Game")
    else:
        print("Not in game")

if args["detection"] == "timer":
    # skip an extra minute ahead
    text = text.split(":")[0]
    frames = 60**2 * (int(text)+1)

    print(f"skipping {frames} frames")

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
