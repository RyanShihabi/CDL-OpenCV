import pytesseract
import cv2

def isClip(players):
    if len(players) < 2:
        return None

    for i in range(0, len(players)):
        for j in range(i+1, len(players)):
            if players[i] == players[j]:
                return players[i]
            else:
                if players[i][1] == players[j][1]:
                    return players[i]

    return None

def secondOfFrame(frame):
    return frame // 60

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

def grabFeed(frame, map, id) -> list:

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

    player = isClip(players)

    if player != None:
        second = secondOfFrame(frame)
            return {"player": player, "clip_range": f"https://www.youtube.com/watch?start={second-5}&end={second+5}&v={id}&ab_channel=CallofDutyLeague", "map": map}
        # Dont need to check if second is less than 5, wont happen games dont start until later

    return None
