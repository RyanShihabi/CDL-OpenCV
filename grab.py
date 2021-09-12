import pytesseract
import cv2

def isClip(text):
    if len(text) < 2:
        return False
    for i in range(0, len(text)):
        for j in range(i+1, len(text)):
            if text[i] == text[j]:
                return True
    return False

def secondOfFrame(frame, fps):
    return frame // fps

def grabMapName(frame) -> str:
    #find ROI

    mapName = frame[:, :]

    width = int(image.shape[1] * 300 / 100)
    height = int(image.shape[0] * 300 / 100)

    dimensions = (width, height)

    scaled_image = cv2.resize(mapName, (width, height), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")

    print(text)

    return text

def grabFeed(frame) -> list:
    #find ROI

    feed = frame[:, :]

    width = int(image.shape[1] * 300 / 100)
    height = int(image.shape[0] * 300 / 100)

    dimensions = (width, height)

    scaled_image = cv2.resize(feed, (width, height), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(frame, 3)

    text = pytesseract.image_to_string(blur, lang="eng", config="--psm 6 --oem 1")

    text = text.split('\n')[:-1]

    print(text)

    if isClip(text):
        second = secondOfFrame(frame, 60)
        if second >= 5:
            clip_range = [second-5, second+5]
        else:
            clip_range = [0, second+5]

    return clip_range
