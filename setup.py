import os
from os import path
import pathlib
import json
import datetime
from grab import *
import cv2

playlist = "PLisfUdjySbZVoTRbAlfObs8dI-cb-gWk-"

timestamp = str(datetime.datetime.now())[:10]

if path.exists(f"data/playlist/{timestamp}.json") == False:
    print("Grabbing playlist information...")
    os.system(f"youtube-dl --dump-single-json {playlist} > data/playlist/{timestamp}.json")

dates = []
earliest_date = ""
for path in pathlib.Path("./data/playlist").iterdir():
    date = str(path)[14:-5]
    dates.append(date)

dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

print(dates)

while len(dates) > 2:
    print("Cleaning list...")
    os.remove(f"data/playlist/{dates[0]}.json")
    dates.pop(0)

f = open(f"data/playlist/{timestamp}.json",)

data = json.load(f)

f.close()

print(len(data["entries"]))

videos = []

for i in data["entries"]:
    videos.append([i['title'], i['id']])

# once video is downloaded, add to completed.txt
completed_videos = []
with open("videos/completed.txt", "r+") as f:
    for line in f.readlines():
        completed_videos.append(line)
f.close()

maps = []
clips = {"clips": []}
for video in videos:
    if video[0] not in completed_videos:
        # Download format: 1080p60, no audio
        # figure out option commands for format and no audio

        # os.system(f"youtube-dl {video[1]}")

        cap = cv2.VideoCapture("videos/FaZeTorontoRaid.mp4")
            while cap.isOpened():
                ret, frame = cap.read()
                cv2.imshow("FaZeTorontoRaid", frame)

                map = grabMap(frame)
                if map != "None":
                    maps.append(map)

                try:
                    clip = grabFeed(frame, maps[-1], video[1])
                    if clip != None:
                        clips["clips"].append(clip)
                        cap.set(cv2.CAP_PROP_POS_FRAMES, )
                        # skip five seconds worth of frames as clips range 5 seconds back and forward
                except IndexError:
                    print("No map detected, can't detect feed")

                #keep the name of the map until the next map appears
                # grabExtra(frame)


            with open("videos/completed.txt", "a+") as f:
                f.write(video[0])
            f.close()
        #determine what metric considers completion
            # json file export or download of the video
            # maybe also use a downloaded.txt to determine what videos still need to be downloaded
            # or put both metrics into one file to save space

with open(f"data/processed/clips.json", "w+") as json_file:
    json.dump(clips, json_file)

json_file.close()
