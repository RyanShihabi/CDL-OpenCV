import pytesseract
import numpy as np
import cv2

class Grab:
    def __init__(self, id, date, map=None):
        self.id = id
        self.date = date
        self.map = map

    def getMap(self):
        return self.map

    def setMap(self, map):
        self.map = map

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

    def grabPlayer(self, frame) -> str:
        player_roi = frame[940:995, 1355:1650]

        (b, g, r) = player_roi[40, 175]

        player_roi = cv2.medianBlur(player_roi, 1)

        gray = cv2.cvtColor(player_roi, cv2.COLOR_BGR2GRAY)

        width = int(gray.shape[1] * 300 / 100)
        height = int(gray.shape[0] * 200 / 100)
        player_roi = cv2.resize(gray, (width, height), interpolation = cv2.INTER_AREA)

        w_thresh = cv2.threshold(player_roi, 180, 255, cv2.THRESH_BINARY_INV)[1]
        b_thresh = cv2.threshold(player_roi, 60, 255, cv2.THRESH_BINARY)[1]

        data = [pytesseract.image_to_string(b_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0].upper(), pytesseract.image_to_string(w_thresh, lang="eng", config="--psm 6 --oem 1").split("\n")[0].upper()]

        if 200 <= b <= 255 and 200 <= g <= 255 and 200 <= r <= 255:
            text = data[0]
        else:
            if len(data[0]) > len(data[1]):
                text = data[0]
            else:
                text = data[1]

        text = "".join(x for x in text if x.isalpha() or x == "6")

        if len(text) == 2 and (text[-1] == "b" or text[-1] == "B"):
            text = text.replace(text[-1], "6")
        elif len(text) > 3 and (text[-2:].lower() == "mp" or text[-3:].lower() == "mip"):
            text = "SIMP"

        return text

    def isClip(self, players, camera) -> list:
        if len(players) < 2:
            return None

        for i in range(0, len(players)):
            for j in range(i+1, len(players)):
                if (camera.lower() in players[i].lower()) and (camera.lower() in players[j].lower()):
                    return players[i]

        return None


    def secondOfFrame(self, frame) -> int:
        return int(frame // 59.94)

    def grabTeams(self, title) -> list:
    # "Ex: Champs Final | @Toronto Ultra vs @Atlanta FaZe | Championship Weekend | Day 4"
        teams = title.split("|")[1].split("@")[1:]
        return [teams[0][:-4], teams[1][:-1]]

    def inGame(self, frame) -> bool:
        roi = frame[1013:1014, 1455:1456]
        b, g, r = roi[0, 0]

        if (150 <= b <= 255) and (150 <= g <= 255) and (106 <= r <= 255):
            return True
        return False


    def grabMapName(self, frame) -> str:
        maps = {"APOCALYPSE": [(38, 720), (520, 1048)],
                "CHECKMATE": [(72, 805), (585, 1018)],
                "EXPRESS": [(45, 742), (520, 1042)],
                "GARRISON": [(50, 780), (575, 1025)],
                "MIAMI": [(50, 700), (420, 1037)],
                "MOSCOW": [(50, 775), (610, 1040)],
                "RAID": [(35, 725), (445, 1040)]}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #720
        # mapName = gray[585:640, 240:550]

        #1080
        map_name_roi = gray[875:975, 345:950]

        thresh = cv2.threshold(map_name_roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        text = pytesseract.image_to_string(thresh, lang="eng", config="--psm 6 --oem 1")
        text = "".join(text.split(" "))

        for map in maps:
            if map in text and maps[map] != self.map:
                print("setting new map:", map)
                self.map = maps[map]
                return True
        return False

    def grabTimer(self, frame) -> int:
        roi = frame[445:725, 550:1400]

        timer_roi = cv2.threshold(np.array(roi), 125, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(timer_roi, lang="eng", config="--psm 7 --oem 1").split(':')[0]

        return 60 * 60 * (int(text)+1)

    def grabFeed(self, frame, fts, camera) -> dict:
        #720 roi
        # feed_roi = frame[350:500, 0:275]
        text = []

        frame = cv2.medianBlur(frame, 1)

        #1080 roi
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

        players = []
        for line in text:
            if len(line) > 4:
                if line[0] in ['[', '(', '|', '{'] or line[4] in [']', ')', '|', '}']:
                    player = line.split(" ")[:2]
                    name = ""

                    if len(player) >= 2:
                        name = "".join(x for x in player[1] if x.isalnum())

                    players.append(f"{player[0]} {name}")

        print(players)
        player = self.isClip(players, camera)

        if player and "C6" in player.split()[1][:2]:
            player = "[DAL] C6"

        try:
            if player != None:
                second = self.secondOfFrame(fts)
                print(f"clip found for {player} at {second}")

                return {"player": player, "frame": fts}

            return None
        except Exception:
            return None
