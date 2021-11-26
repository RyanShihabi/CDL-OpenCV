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

if args["detection"] == "player":
    # player_roi = image[940:990, 1355:1650]
    player_roi = image[935:995, 1355:1650]

    gray = cv2.cvtColor(player_roi, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    adapt = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,99,3)

    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # lower_black = np.array([0,0,0])
    # upper_black = np.array([10,10,10])
    # mask = cv2.inRange(hsv, lower_black, upper_black)
    # res = cv2.bitwise_and(frame,frame, mask=mask)

    # w_thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    # b_thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

    # thresh = cv2.threshold(gray, 30, 0, cv2.THRESH_BINARY_INV)[1]

    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename, adapt)
    cv2.imshow("Output", adapt)
    # cv2.imshow("Output", w_thresh)
    # cv2.imshow("Output", b_thresh)

    # w_text = pytesseract.image_to_string(w_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0]
    # b_text = pytesseract.image_to_string(b_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0]
    text = pytesseract.image_to_string(adapt, lang="eng", config="--psm 6 --oem 1").split("\n")[0]

    # text = w_text+b_text

    # text = "".join(x for x in text if x.isalpha() or x == "6")

    print(text)
    print(len(text))


if args["detection"] == "map":
    #720p roi
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #1080
    map_roi = gray[775:1079, 45:910]

    thresh = cv2.threshold(map_roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    filename = f"{os.getpid()}.png"
    cv2.imwrite(filename, thresh)
    cv2.imshow("Output", thresh)

if args["detection"] == "feed":
    #720p roi
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    feed_roi = image[500:700, 0:175]

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
    # there may be a better roi
    roi = image[1013:1014, 1455:1456]
    b, g, r = roi[0, 0]
    print([b, g, r])
    # width = int(roi.shape[1] * 250 / 100)
    # height = int(roi.shape[0] * 250 / 100)
    #
    # roi = cv2.resize(roi, (width, height), interpolation = cv2.INTER_AREA)
    # # roi = cv2.medianBlur(roi, 3)
    #
    # # roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]
    filename = f"{os.getpid()}.png"

    cv2.imwrite(filename, roi)
    cv2.imshow("game", roi)

text = pytesseract.image_to_string(Image.open(filename), lang="eng", config="--psm 6 --oem 1")
os.remove(filename)
print(text)

cv2.waitKey(0)

if args["detection"] == "player":
    text = text.split("\n")[0]
    text = "".join(x for x in text if x.isalpha() or x == "6")
    print(text)
    print(len(text))

if args["detection"] == "game":
    # modes = ["CONTROL", "HARDPOINT", "SEARCH & DESTROY", "SND"] #find other game modes, test mutltiple roi

    # text = text.split("\n")[0]

    if b == 204 and g == 199 and r == 202:
        print("In Game")
    else:
        print("Not in game")

    # if text in modes:
    #     print("In Game")
    # else:
    #     print("Not in game")

if args["detection"] == "timer":
    # skip an extra minute ahead
    text = text.split(":")[0]
    frames = 60**2 * (int(text)+1)

    print(f"skipping {frames} frames")

if args["detection"] == "map":
    maps = {"RAID": [(30, 725), (450, 1045)], "GARRISON": [(50, 780), (575, 1025)]}
    text = "".join(text.split(" "))
    print(text)
    for map in maps:
        if map in text:
            print(maps[map])

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
