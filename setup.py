import os
from os import path
import pathlib
import json
import datetime
import numpy as np
import grab
import cv2

# start downloading videos
#

def grabTeamColors(frame) -> list:
    colors = []
    dim_threshold = 2.3
    bright_threshold = 2.65

    team1_roi = frame[25:60, 300:350]
    team2_roi = frame[25:60, 1550:1600]

    team1_color_b, team1_color_g, team1_color_r = team1_roi[16, 24]
    team2_color_b, team2_color_g, team2_color_r = team2_roi[16, 24]

    if (team1_color_b >= 255-55) and (team1_color_g >= 255-55) and (team1_color_r >= 255-55):
        team1_bounds = [np.array([np.maximum(0, team1_color_b-50), np.maximum(0, team1_color_g-50), np.maximum(0, team1_color_r-50)]), np.array([np.minimum(255, team1_color_b+50), np.minimum(255, team1_color_g+50), np.minimum(255, team1_color_r+50)])]
        colors.append({"bounds": team1_bounds, "color_space": "HLS"})
    else:
        team1_color_b_min = np.maximum(0, int(team1_color_b / dim_threshold))
        team1_color_g_min = np.maximum(0, int(team1_color_g / dim_threshold))
        team1_color_r_min = np.maximum(0, int(team1_color_r / dim_threshold))

        team1_color_b_max = np.minimum(255, int(team1_color_b * bright_threshold))
        team1_color_g_max = np.minimum(255, int(team1_color_g * bright_threshold))
        team1_color_r_max = np.minimum(255, int(team1_color_r * bright_threshold))

        team1_bounds = [np.array([team1_color_b_min, team1_color_g_min, team1_color_r_min]), np.array([team1_color_b_max, team1_color_g_max, team1_color_r_max])]
        print(team1_bounds)
        colors.append({"bounds": team1_bounds, "color_space": "BGR"})

    if (team2_color_b >= 255-55) and (team2_color_g >= 255-55) and (team2_color_r >= 255-55):
        team2_bounds = [np.array([np.maximum(0, team2_color_b-50), np.maximum(0, team2_color_g-50), np.maximum(0, team2_color_r-50)]), np.array([np.minimum(255, team2_color_b+50), np.minimum(255, team2_color_g+50), np.minimum(255, team2_color_r+50)])]
        colors.append({"bounds": team2_bounds, "color_space": "HLS"})
    else:
        team2_color_b_min = np.maximum(0, int(team2_color_b / dim_threshold))
        team2_color_g_min = np.maximum(0, int(team2_color_g / dim_threshold))
        team2_color_r_min = np.maximum(0, int(team2_color_r / dim_threshold))

        team2_color_b_max = np.minimum(255, int(team2_color_b * bright_threshold))
        team2_color_g_max = np.minimum(255, int(team2_color_g * bright_threshold))
        team2_color_r_max = np.minimum(255, int(team2_color_r * bright_threshold))

        team2_bounds = [np.array([team2_color_b_min, team2_color_g_min, team2_color_r_min]), np.array([team2_color_b_max, team2_color_g_max, team2_color_r_max])]
        print(team2_bounds)
        colors.append({"bounds": team2_bounds, "color_space": "BGR"})

    return colors


teams = []
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

def grabTeams(self, title) -> list:
# "Champs Final | @Toronto Ultra vs @Atlanta FaZe | Championship Weekend | Day 4"
    teams = title.split("|")[1].split("@")[1:]
    return [teams[0][:-4], teams[1][:-1]]

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

    maps = []
    clips = {"clips": []}
    grab = Grab()
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

                    if (frame_count % 30 == 0) and (len(colors) > 0) and (len(maps) == rounds):
                        try:
                            clip = grab.grabFeed(frame, maps[-1], "TestVideo", frame_count)
                            if clip != None:
                                print("clip found")
                                clips["clips"].append(clip)
                                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + 300)
                                frame_count += 300
                                # skip five seconds worth of frames as clips range 5 seconds back and forward
                                # 5 seconds in terms of 60 frames per second
                        except Exception as e:
                            print(e)
                    else:
                        if frame_count % 30 == 0:
                            map = grab.grabMapName(frame)

                            if map != "None":
                                print("Map detected:", map)
                                maps.append(map)
                                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + map_skip)
                                frame_count += map_skip
                                continue

                            if len(maps) == rounds:
                                colors = grabTeamColors(frame)
                                print(colors)
                                grab.setBounds(colors)

                    cv2.imshow("Frame", frame)
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
