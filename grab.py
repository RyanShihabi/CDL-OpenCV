import pytesseract
import numpy as np
import imutils
import cv2

class Grab:
    def __init__(self, bounds=[{'bounds': [np.array([57,  91, 255], dtype=np.uint8), np.array([56,  90, 255], dtype=np.uint8)], 'color_space': 'BGR'}, {'bounds': [np.array([255, 255, 255], dtype=np.uint8), np.array([255, 255, 255], dtype=np.uint8)], 'color_space': 'HLS'}]):
        self.bounds = bounds

    def getBounds(self):
        return self.bounds

    def setBounds(self, bounds):
        print("setting bounds")
        self.bounds = bounds

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

    def inGame(self, frame) -> bool:
        modes = ["CONTROL", "HARDPOINT", "SEARCH & DESTROY", "SND"] #find other game modes, test mutltiple roi

        roi = frame[150:200, 900:1050]
        width = int(roi.shape[1] * 250 / 100)
        height = int(roi.shape[0] * 250 / 100)

        roi = cv2.resize(roi, (width, height), interpolation = cv2.INTER_AREA)
        roi = cv2.medianBlur(roi, 3)

        roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(roi, lang="eng", config="--psm 6 --oem 1")

        text = text.split("\n")[0]

        if text in modes:
            return True

        return False


    def grabMapName(self, frame) -> str:
        maps = ["RAID", "GARRISON"]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #720
        # mapName = gray[585:640, 240:550]

        #1080
        mapName = gray[875:975, 345:900]

        # cv2.imshow("Map", mapName)

        text = pytesseract.image_to_string(mapName, lang="eng", config="--psm 6 --oem 1")


        text = text.split(" ")[0]

        # full_text = pytesseract.image_to_string(frame, lang="eng", config="--psm 6 --oem 1")
        #
        # text = text.split(" ")[0]

        print(text)

        for map in maps:
            if text == map:
                return map
        return "None"

    def grabTimer(self, frame) -> int:
        roi = frame[445:725, 550:1400]

        timer_roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(timer_roi, lang="eng", config="--psm 7 --oem 1")
        text = text.split(':')[0]

        return 60 * 60 * (int(text)+1)

    def grabFeed(self, frame, id, fts) -> dict:
        #720 roi
        # feed_roi = frame[350:500, 0:275]
        text = []

        #1080 roi
        feed_roi = frame[500:700, 0:175]

        width = int(feed_roi.shape[1] * 200 / 100)
        height = int(feed_roi.shape[0] * 200 / 100)

        feed_roi = cv2.resize(feed_roi, (width, height), interpolation = cv2.INTER_AREA)

        team1_lower = self.bounds[0]["bounds"][0]
        team1_upper = self.bounds[0]["bounds"][1]

        if self.bounds[0]["color_space"] == "BGR":
            mask_team1 = cv2.inRange(feed_roi, team1_lower, team1_upper)

            res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team1)

            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

            blur = cv2.medianBlur(gray, 1)

            #OTSU
            # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)

        elif self.bounds[0]["color_space"] == "HLS":
            hls = cv2.cvtColor(feed_roi, cv2.COLOR_BGR2HLS)
            light = hls[:, :, 1]

            mask_team1 = cv2.inRange(light, 200, 255)

            res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team1)

            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)

        else:
            print("no color space format detected")

        #OTSU
        # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # print(thresh)
        cv2.imshow("Team 1", thresh)

        team1_text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")
        team1_text = team1_text.split('\n')[:-1]

        text.append(team1_text)

        team2_lower = self.bounds[1]["bounds"][0]
        team2_upper = self.bounds[1]["bounds"][1]

        if self.bounds[1]["color_space"] == "BGR":
            mask_team2 = cv2.inRange(feed_roi, team2_lower, team2_upper)

            res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team2)

            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

            blur = cv2.medianBlur(gray, 1)

            #OTSU
            # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)


        elif self.bounds[1]["color_space"] == "HLS":
            hls = cv2.cvtColor(feed_roi, cv2.COLOR_BGR2HLS)
            light = hls[:, :, 1]

            # bgr_lower = self.bounds[1]["bounds"][0]
            # bgr_upper = self.bounds[1]["bounds"][1]

            mask_team2 = cv2.inRange(light, 220, 255)

            res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team2)

            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)
        else:
            print("no color space format detected")

        cv2.imshow("Team 2", thresh)

        # kernel = np.ones((3,3), np.uint8)
        # erosion = cv2.erode(thresh, kernel, iterations=1)
        # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        # gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

        # cv2.imshow("feed", erosion)

        team2_text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")
        team2_text = team2_text.split('\n')[:-1]

        text.append(team2_text)

        print(text)

        # players format [['clan tag', 'gamertag'], ...]
        players = []
        for lines in text:
            for line in lines:
                if len(line) > 4:
                    if line[0] in ['[', '(', '|', '{'] or line[4] in [']', ')', '|', '}']:
                        # make it so the brackets dont make it into the clan abbreviation
                        players.append(line.split(" ")[:2])

        # print(players)
        player = self.isClip(players)

        if player != None:
            second = self.secondOfFrame(fts)
            # keep clan name?
            return {"player": player, "clip_range": f"https://www.youtube.com/watch?start={second-5}&end={second+5}&v={id}&ab_channel=CallofDutyLeague"}
            # Dont need to check if second is less than 5, wont happen games dont start until later

        return None
