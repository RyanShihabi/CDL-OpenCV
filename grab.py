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

def grabMapName(frame, map) -> str:
    #find ROI
    width = int(frame.shape[1] * 300 / 100)
    height = int(frame.shape[0] * 300 / 100)

    dimensions = (width, height)

    scaled_image = cv2.resize(mapName, (width, height), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
    mapName = scaled_image[2650:2875, 1075:2500]
    thresh = cv2.threshold(mapName, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")

    print(text)

    if text not in maps:
        return "None"
    else:
        return text

def grabFeed(frame, map) -> list:

    feed = frame[1300:2100, 0:1100]

    width = int(image.shape[1] * 300 / 100)
    height = int(image.shape[0] * 300 / 100)

    dimensions = (width, height)

    scaled_image = cv2.resize(feed, (width, height), interpolation = cv2.INTER_AREA)
    blur = cv2.medianBlur(scaled_image, 3)

    text = pytesseract.image_to_string(blur, lang="eng", config="--psm 6 --oem 1")

    text = text.split('\n')[:-1]

    # players format [['clan tag', 'gamertag'], ...]
    players = []
    for line in text:
        if line[0] == '[' or line[4] == ']':
            players.append(line.split(" ")[:2])

    return players

    if isClip(text):
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
        # clip_range = [second-5, second+5]

        # check if a map has been found
        # make sure the map is not the same as well
            # make sure map isnt the same as the last
        # upload youtube url to d
