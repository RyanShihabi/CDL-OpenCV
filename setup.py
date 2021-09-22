import os
from os import path
import pathlib
import json
import datetime
import numpy as np
import grab
import cv2

teams = {"Toronto Ultra": {"bounds": [np.array([0, 175, 0]), np.array([255, 255, 255])], "color_space": "HLS"},
        "Atlanta FaZe": {"bounds": [np.array([65, 72, 110]), np.array([119, 133, 206])], "color_space": "BGR"}}
        # "Dallas Empire": {"bounds": [], "color_space": "BGR"},
        # "Florida Mutineers": {"bounds": [], "color_space": "BGR"},
        # "London Royal Ravens": {"bounds": [], "color_space": "BGR"},
        # "Los Angeles Guerrillas": {"bounds": [], "color_space": "BGR"},
        # "Los Angeles Thieves": {"bounds": [], "color_space": "BGR"},
        # "Minnesota ": {"bounds": [], "color_space": "BGR"},
        # "New York Subliners": {"bounds": [], "color_space": "BGR"},
        # "Paris Legion": {"bounds": [], "color_space": "BGR"},
        # "Seattle Surge": {"bounds": [], "color_space": "BGR"},
        # "Optic Chicago": {"bounds": [], "color_space": "BGR"}}

teamHSV = {"Toronto Ultra": [np.array([0, 0, 177], np.uint8), np.array([179, 55, 255], np.uint8)],
            "Atlanta FaZe": [np.array([0, 68, 120], np.uint8), np.array([179, 205, 255], np.uint8)]}

def grabTeamHSV(title):
# "Champs Final | @Toronto Ultra vs @Atlanta FaZe | Championship Weekend | Day 4"
    teams = title.split("|")[1].split("@")[1:]
    return [teamHSV[teams[0][:-4]], teamHSV[teams[1][:-1]]]

def main():
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

    maps = ""
    clips = {"clips": []}
    for video in videos:
        if video[0] not in completed_videos:
            hsv_values = grabTeamHSV(video[0])
            grab = Grab(hsv_values)
            # Trying 720p30 with no audio to see if performance increases format code 136
            # Feeds may need 1080: yes format code 299
            # figure out option commands for format and no audio
            if path.isfile(f"{video[0]}.mp4") == False;
                os.system(f"youtube-dl -f 299 {video[1]}")


            cap = cv2.VideoCapture(f"videos/{video[0]}.mp4")
            frame_count = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    cv2.imshow("FaZeTorontoRaid", frame)

                    # find a way to not ping the map continuously, do once finished with entire program
                    map = grab.grabMap(frame)

                    if map != "None":
                        maps.append(map)
                        map_current = map

                    try:
                        clip = grab.grabFeed(frame, maps[-1], video[1])
                        # clip = grab.grabFeed(frame, map_current, video[1])

                        if clip != None:
                            clips["clips"].append(clip)
                            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count += 300)
                            # skip five seconds worth of frames as clips range 5 seconds back and forward
                    except IndexError:
                        print("No map detected, can't detect feed")

                    frame_count += 1


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

if __name__ == "__main__":
    main()
