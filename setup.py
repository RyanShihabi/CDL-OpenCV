import os
from os import path
import json
import datetime

playlist = "PLisfUdjySbZVoTRbAlfObs8dI-cb-gWk-"

timestamp = str(datetime.datetime.now())[:10]

if path.exists(f"data/{timestamp}.json") == False:
    print("Grabbing playlist information...")
    os.system(f"youtube-dl --dump-single-json {playlist} > data/{timestamp}.json")

f = open(f"data/{timestamp}.json",)

data = json.load(f)

f.close()

print(len(data["entries"]))

videos = []

for i in data["entries"]:
    videos.append([i['title'], i['id']])

print(videos)

# once video is downloaded, add to downloaded.txt
