import pytesseract
import numpy as np
import imutils
import datetime
import cv2

class Grab:
    def __init__(self, id, date, bounds=None):
        self.bounds = bounds
        self.id = id
        self.date = date

    def getBounds(self) -> list:
        return self.bounds

    def setBounds(self, bounds):
        self.bounds = bounds

    def setId(self, id):
        print("setting id")
        self.id = id

    def getId(self):
        return self.id

    def setDate(self, date):
        print("setting date")
        self.date = date

    def getDate(self):
        return self.date

    # def setBounds(self, bounds):
    #     print("setting bounds")
    #     self.bounds = bounds

    def grabPlayer(self, frame) -> str:
        # [940:995, 1355:1650]
        player_roi = frame[940:995, 1355:1650]

        (b, g, r) = player_roi[40, 175]

        player_roi = cv2.medianBlur(player_roi, 1)

        gray = cv2.cvtColor(player_roi, cv2.COLOR_BGR2GRAY)

        width = int(gray.shape[1] * 300 / 100)
        height = int(gray.shape[0] * 200 / 100)
        player_roi = cv2.resize(gray, (width, height), interpolation = cv2.INTER_AREA)

        w_thresh = cv2.threshold(player_roi, 180, 255, cv2.THRESH_BINARY_INV)[1]
        b_thresh = cv2.threshold(player_roi, 60, 255, cv2.THRESH_BINARY)[1]

        # print(b)

        # cv2.imshow("w_banner", w_thresh)
        # cv2.imshow("b_banner", b_thresh)

        # cv2.waitKey(1)

        # w_text = pytesseract.image_to_string(w_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0]
        # b_text = pytesseract.image_to_string(b_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0]
        #
        # if w_text == b_text:
        #     text = w_text
        # else:
        #     text = w_text+b_text

        data = [pytesseract.image_to_string(b_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0].upper(), pytesseract.image_to_string(w_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0].upper()]
        # print(data)

        # if len(data[0]) > len(data[1]):
        #     text = data[0]
        # else:
        #     text = data[1]

        if 200 <= b <= 255 and 200 <= g <= 255 and 200 <= r <= 255:
            text = data[0]
            # text = pytesseract.image_to_string(b_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0].upper()
        else:
            # text = pytesseract.image_to_string(w_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0].upper()
            if len(data[0]) > len(data[1]):
                text = data[0]
            else:
                text = data[1]

        text = "".join(x for x in text if x.isalpha() or x == "6")

        if len(text) == 2 and text[-1] == "b":
            text = text.replace("b", "6")
        elif len(text) > 3 and (text[-2:].lower() == "mp" or text[-3:].lower() == "mip"):
            text = "SIMP"

        # print(text)
        return text

    def isClip(self, players) -> list:
        if len(players) < 2:
            return None

        for i in range(0, len(players)):
            for j in range(i+1, len(players)):
                if players[i][6:].lower() == players[j][6:].lower():
                    return players[i]

        return None


    def secondOfFrame(self, frame) -> int:
        return int(frame // 59.94)

    def grabTeams(self, title) -> list:
    # "Champs Final | @Toronto Ultra vs @Atlanta FaZe | Championship Weekend | Day 4"
        teams = title.split("|")[1].split("@")[1:]
        return [teams[0][:-4], teams[1][:-1]]

    def inGame(self, frame) -> bool:
        # modes = ["CONTROL", "HARDPOINT", "SEARCH & DESTROY", "SND"] #find other game modes, test mutltiple roi

        # roi = frame[150:200, 900:1050]
        # width = int(roi.shape[1] * 250 / 100)
        # height = int(roi.shape[0] * 250 / 100)
        #
        # roi = cv2.resize(roi, (width, height), interpolation = cv2.INTER_AREA)
        # roi = cv2.medianBlur(roi, 3)
        #
        # roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]
        #
        # cv2.imshow("mode", roi)
        #
        # text = pytesseract.image_to_string(roi, lang="eng", config="--psm 6 --oem 1")
        #
        # text = text.split("\n")[0]

        # figure out why UI changes background color randomly

        roi = frame[1013:1014, 1455:1456]
        b, g, r = roi[0, 0]
        # print([b, g, r])

        if (150 <= b <= 255) and (150 <= g <= 255) and (106 <= r <= 255):
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

        text = pytesseract.image_to_string(mapName, lang="eng", config="--psm 6 --oem 1").split(" ")[0]


        # text = text.split(" ")[0]

        # full_text = pytesseract.image_to_string(frame, lang="eng", config="--psm 6 --oem 1")
        #
        # text = text.split(" ")[0]

        # print(text)

        for map in maps:
            if text == map:
                return map
        return "None"

    def grabTimer(self, frame) -> int:
        roi = frame[445:725, 550:1400]

        timer_roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(timer_roi, lang="eng", config="--psm 7 --oem 1").split(':')[0]
        # text = text.split(':')[0]

        return 60 * 60 * (int(text)+1)

    def grabFeed(self, frame, fts, camera) -> dict:
        #720 roi
        # feed_roi = frame[350:500, 0:275]
        text = []
        # print("running")

        frame = cv2.medianBlur(frame, 1)

        #1080 roi
        # original: [500:700, 0:175]
        pos1 = frame[630:670, 0:230]
        pos2 = frame[595:635, 0:230]
        pos3 = frame[560:600, 0:230]

        width = int(pos1.shape[1] * 200 / 100)
        height = int(pos1.shape[0] * 200 / 100)
        pos1 = cv2.resize(pos1, (width, height), interpolation = cv2.INTER_AREA)

        width = int(pos2.shape[1] * 200 / 100)
        height = int(pos2.shape[0] * 200 / 100)
        pos2 = cv2.resize(pos2, (width, height), interpolation = cv2.INTER_AREA)

        width = int(pos3.shape[1] * 200 / 100)
        height = int(pos3.shape[0] * 200 / 100)
        pos3 = cv2.resize(pos3, (width, height), interpolation = cv2.INTER_AREA)

        textP1 = pytesseract.image_to_string(pos1, lang="eng", config="--psm 6 --oem 1").split('\n')[0]
        text.append(textP1)

        textP2 = pytesseract.image_to_string(pos2, lang="eng", config="--psm 6 --oem 1").split('\n')[0]
        text.append(textP2)

        textP3 = pytesseract.image_to_string(pos3, lang="eng", config="--psm 6 --oem 1").split('\n')[0]
        text.append(textP3)
        # text = text.split('\n')[:-1]


        # team1_lower = self.bounds[0]["bounds"][0]
        # team1_upper = self.bounds[0]["bounds"][1]
        #
        # if self.bounds[0]["color_space"] == "BGR":
        #     mask_team1 = cv2.inRange(feed_roi, team1_lower, team1_upper)
        #
        #     res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team1)
        #
        #     gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        #
        #     blur = cv2.medianBlur(gray, 1)
        #
        #     #OTSU
        #     # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #
        #     thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)
        #
        # elif self.bounds[0]["color_space"] == "HLS":
        #     hls = cv2.cvtColor(feed_roi, cv2.COLOR_BGR2HLS)
        #     light = hls[:, :, 1]
        #
        #     mask_team1 = cv2.inRange(light, 200, 255)
        #
        #     res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team1)
        #
        #     gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        #
        #     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)
        #
        # else:
        #     print("no color space format detected")
        #
        # #OTSU
        # # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # # print(thresh)
        # cv2.imshow("Team 1", feed_roi)
        #
        # team1_text = pytesseract.image_to_string(feed_roi, lang="eng", config="--psm 6 --oem 1")
        # team1_text = team1_text.split('\n')[:-1]
        #
        # text.append(team1_text)
        #
        # team2_lower = self.bounds[1]["bounds"][0]
        # team2_upper = self.bounds[1]["bounds"][1]
        #
        # if self.bounds[1]["color_space"] == "BGR":
        #     mask_team2 = cv2.inRange(feed_roi, team2_lower, team2_upper)
        #
        #     res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team2)
        #
        #     gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        #
        #     blur = cv2.medianBlur(gray, 1)
        #
        #     #OTSU
        #     # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #
        #     thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)
        #
        #
        # elif self.bounds[1]["color_space"] == "HLS":
        #     hls = cv2.cvtColor(feed_roi, cv2.COLOR_BGR2HLS)
        #     light = hls[:, :, 1]
        #
        #     # bgr_lower = self.bounds[1]["bounds"][0]
        #     # bgr_upper = self.bounds[1]["bounds"][1]
        #
        #     mask_team2 = cv2.inRange(light, 220, 255)
        #
        #     res = cv2.bitwise_or(feed_roi, feed_roi, mask=mask_team2)
        #
        #     gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        #
        #     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 71, 1)
        # else:
        #     print("no color space format detected")

        # cv2.imshow("Team 2", thresh)

        # kernel = np.ones((3,3), np.uint8)
        # erosion = cv2.erode(thresh, kernel, iterations=1)
        # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        # gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

        # cv2.imshow("feed", erosion)

        # team2_text = pytesseract.image_to_string(feed_roi, lang="eng", config="--psm 6 --oem 1")
        # team2_text = team2_text.split('\n')[:-1]
        #
        # text.append(team2_text)

        # players format [['clan tag', 'gamertag'], ...]
        # print(text)

        players = []
        for line in text:
            # for line in lines:
            if len(line) > 4:
                if line[0] in ['[', '(', '|', '{'] or line[4] in [']', ')', '|', '}']:
                    player = line.split(" ")[:2]
                    name = ""

                    if len(player) >= 2:
                        name = "".join(x for x in player[1] if x.isalnum())

                    players.append(f"{player[0]} {name}")

        print(players)
        player = self.isClip(players)

        if player != None and camera.lower() == player[6:].lower():
            second = self.secondOfFrame(fts)
            print(f"clip found for {player} at {second}")
            # keep clan name?
            # "https://www.youtube.com/embed/OTsYiHhrDPw?&start=692&end=702"

            # return {"player": player, "clip_url": f"https://www.youtube.com/embed/{self.id}?&start={second-8}&end={second+8}", "date": self.date}
            return {"player": player, "frame": fts}
            # Dont need to check if second is less than 5, wont happen games dont start until later

        return None
