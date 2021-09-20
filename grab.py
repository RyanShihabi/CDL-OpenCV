import pytesseract
import numpy as np
import cv2

class Grab:
    def __init__(self, bounds):
        self.bounds = bounds
        print(self.bounds)

    def isClip(self, players) -> list:
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

    def secondOfFrame(self, frame) -> int:
        return frame // 60

    def grabTeams(self, title) -> list:
    # "Champs Final | @Toronto Ultra vs @Atlanta FaZe | Championship Weekend | Day 4"
        teams = title.split("|")[1].split("@")[1:]
        return [teams[0][:-4], teams[1][:-1]]

    def grabMapName(self, frame) -> str:
        maps = ["RAID", "GARRISON"]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #720
        # mapName = gray[585:640, 240:550]

        #1080
        mapName = gray[875:975, 345:900]

        text = pytesseract.image_to_string(mapName, lang="eng", config="--psm 6 --oem 1")

        text = text.split(" ")[0]

        for map in maps:
            if text == map:
                return map
        return "None"

    def grabFeed(self, frame, map, id, fts) -> dict:
        #720 roi
        # feed_roi = frame[350:500, 0:275]

        text = []

        #1080 roi
        feed_roi = frame[500:700, 0:175]

        width = int(feed_roi.shape[1] * 200 / 100)
        height = int(feed_roi.shape[0] * 200 / 100)

        feed_roi = cv2.resize(feed_roi, (width, height), interpolation = cv2.INTER_AREA)

        team1_lower = self.bounds[1][0]
        team1_upper = self.bounds[1][1]

        mask_team1 = cv2.inRange(feed_roi, team1_lower, team1_upper)

        res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team1)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        blur = cv2.medianBlur(gray, 1)

        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)

        cv2.imshow("Atlanta FaZe", thresh)

        textBGR = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")
        textBGR = textBGR.split('\n')[:-1]

        text.append(textBGR)

        hls = cv2.cvtColor(feed_roi, cv2.COLOR_BGR2HLS)

        light = hls[:,:,1]

        team2_lower = self.bounds[0][0]
        team2_upper = self.bounds[0][1]

        mask_team2 = cv2.inRange(hls, team2_lower, team2_upper)

        res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team2)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)

        cv2.imshow("Toronto Ultra", thresh)

        # kernel = np.ones((3,3), np.uint8)
        # erosion = cv2.erode(thresh, kernel, iterations=1)
        # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        # gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

        # cv2.imshow("feed", erosion)

        textHLS = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")
        textHLS = textHLS.split('\n')[:-1]

        text.append(textHLS)

        cv2.imshow("Feed", feed_roi)

        text = pytesseract.image_to_string(feed_roi, lang="eng", config="--psm 6 --oem 1")
        text = text.split('\n')[:-1]

        print(text)

        # players format [['clan tag', 'gamertag'], ...]
        players = []
        # for lines in text:
        for line in lines:
            if len(line) > 4:
                if line[0] in ['[', '(', '|', '{'] or line[4] in [']', ')', '|', '}']:
                    # make it so the brackets dont make it into the clan abbreviation
                    players.append(line.split(" ")[:2])

        # print(players)
        player = self.isClip(players)

        if player != None:
            second = self.secondOfFrame(fts)
            return {"player": player, "clip_range": f"https://www.youtube.com/watch?start={second-5}&end={second+5}&v={id}&ab_channel=CallofDutyLeague", "map": map}
            # Dont need to check if second is less than 5, wont happen games dont start until later

        return None
