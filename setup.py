import os
from os import path
import pathlib
import json
import datetime

file_count = 0

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

# print("Num of files: ", file_count){value for value in variable}

f = open(f"data/playlist/{timestamp}.json",)

data = json.load(f)

f.close()

print(len(data["entries"]))

videos = []

for i in data["entries"]:
    videos.append([i['title'], i['id']])

# print(videos)

# once video is downloaded, add to downloaded.txt
