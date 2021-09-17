from PIL import Image
import pytesseract
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="input image path for OCR")
ap.add_argument("-d", "--detection", help="choose text to detect")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

print((image.shape[1], image.shape[0]))

# try resizing the image to get broader pixel values
# You only need to look on the left side of the kill feed. That determines a clip

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Map text detection works best with blur filter
# Kill feed text detects best with blur filter
# figure out if there are better blur methods
# maybe start using masking to filter out unwanted COLOR
# test kill feed on multiple scenarios
    # five players on feed

if args["detection"] == "map":
    #720p roi
    map_roi = image[585:640, 240:550]
    gray = cv2.cvtColor(map_roi, cv2.COLOR_BGR2GRAY)

elif args["detection"] == "feed":
    #720p roi
    # gray_roi = scaled_image[,]
    pass
else:
    gray_roi = gray

filename = f"{os.getpid()}.png"
cv2.imwrite(filename, gray)

text = pytesseract.image_to_string(Image.open(filename), lang="eng", config="--psm 6 --oem 1")
os.remove(filename)
print(text)

# cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)

if args["detection"] == "map":
    text = text.split("-")[0]
if args["detection"] == "feed":
    text = text.split('\n')[:-1]
    # players format [['clan tag', 'gamertag'], ...]
    players = []
    for line in text:
        if line[0] == '[':
            players.append(line.split(" ")[:2])

    print(players)
    print(isClip(players))
    # print(isClip([['[ATL]', 'gamertag'], ['(Atl]', 'gamertag']]))
