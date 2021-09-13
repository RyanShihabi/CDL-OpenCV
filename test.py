from PIL import Image
import pytesseract
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="input image path for OCR")
ap.add_argument("-p", "--preprocess", help="method of preprocessing")
ap.add_argument("-d", "--detection", help="choose text to detect")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

scale = 300
width = int(image.shape[1] * scale / 100)
height = int(image.shape[0] * scale / 100)

dimensions = (width, height)

scaled_image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

def isClip(text):
    if len(text) < 2:
        return False
    for i in range(0, len(text)):
        for j in range(i+1, len(text)):
            if text[i] == text[j]:
                return True
            else:
                if text[i][1] == text[j][1]:
                    return True
    return False

def secondOfFrame(frame, fps):
    return frame // fps

def grabMap(image):
    pass

def grabFeed(image):
    pass


# try resizing the image to get broader pixel values
# You only need to look on the left side of the kill feed. That determines a clip

gray = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)

# Map text detection works best with thresh filter
# Kill feed text detects best with blur filter

if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)
else:
    gray = scaled_image

if args["detection"] == "map":
    gray_roi = gray[2650:2875, 1075:2500]
elif args["detection"] == "feed":
    gray_roi = scaled_image[1300:2100,0:1100]
    # [1300:2100,0:1000]
else:
    gray_roi = gray

filename = f"{os.getpid()}.png"
cv2.imwrite(filename, gray_roi)

text = pytesseract.image_to_string(Image.open(filename), lang="eng", config="--psm 6 --oem 1")
os.remove(filename)
print(text)

cv2.imshow("Image", image)
cv2.imshow("Output", gray_roi)
cv2.waitKey(0)

if args["detection"] == "map":
    text = text.split("*")[0]
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
