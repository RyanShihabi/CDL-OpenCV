import os
from os import path
import pathlib
import json
import datetime
import numpy as np
from pymongo import MongoClient
from pprint import pprint
from grab import Grab
import cv2

client = MongoClient('mongodb+srv://admin:7pPNMQZHfblHXlUg@cdlcluster.shvz6.mongodb.net/CDL?retryWrites=true&w=majority')

db = client.CDL
playerCol = db.Players

serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)

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

# teamHSV = {"Toronto Ultra": [np.array([0, 0, 177], np.uint8), np.array([179, 55, 255], np.uint8)],
#             "Atlanta FaZe": [np.array([0, 68, 120], np.uint8), np.array([179, 205, 255], np.uint8)]}

def grabTeams(self, title) -> list:
# "Champs Final | @Toronto Ultra vs @Atlanta FaZe | Championship Weekend | Day 4"
    teams = title.split("|")[1].split("@")[1:]
    return [teams[0][:-4], teams[1][:-1]]

def main():
    playlist = "PLisfUdjySbZVoTRbAlfObs8dI-cb-gWk-"
    colors = []
    inGame = False
    intro_skip = 600

    timestamp = str(datetime.datetime.now())[:10]

    if os.path.exists(f"../data/playlist/{timestamp}.json") == False:
        print("Grabbing playlist information...")
        os.system(f"yt-dlp --dump-single-json {playlist} > ../data/playlist/{timestamp}.json")

    f = open(f"../data/playlist/{timestamp}.json",)

    data = json.load(f)

    f.close()

    print(len(data["entries"]))

    videos = []

    for i in data["entries"]:
        videos.append([i['title'], i['id'], i['upload_date']])

    # check for completed videos
    completed_videos = []
    with open("../data/processed/completed.txt", "r+") as f:
        for line in f:
            completed_videos.append(line.split("\n")[0])
    f.close()

    # maps = []
    clips = {"Players": []}
    for video in videos:
        if video[0] not in completed_videos:
            grab = Grab(video[1], video[2])
            # Trying 720p30 with no audio to see if performance increases format code 136
            # Feeds may need 1080: format code 299
            # figure out option commands for format and no audio
            if path.isfile(f"videos/{video[0]}.mp4") == False:
                os.system(f"yt-dlp -f 299 {video[1]} -o '~/Desktop/CS/CDL OpenCV/CV/videos/{video[0]}.mp4'")
            # Implement time extraction
            # Make sure the download is cancelled if not completed

            cap = cv2.VideoCapture(f"videos/{video[0]}.mp4")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 24000)
            frame_count = 24000
            prevPlayer = None
            currPlayer = None
            nameRange = {}
            temp_clips = []
            clipFound = False

            print("Starting video:", video[0])

            while cap.isOpened():
                ret, frame = cap.read()

                # only grab feed if team colors are initiated
                # how will you figure out if you are inGame once a round is finished
                if ret:
                    # inGame = grab.inGame(frame)
                    # cv2.imshow("Frame", frame)
                    if (frame_count % 30 == 0) and (len(colors) > 0):
                        inGame = grab.inGame(frame)
                        if inGame:
                            currPlayer = grab.grabPlayer(frame)

                            # try:
                            clip = grab.grabFeed(frame, frame_count, currPlayer)
                            if clip != None:
                                clipFound = True
                                print("clip found")
                                temp_clips.append(clip)
                                    # skip five seconds worth of frames as clips range 5 seconds back and forward
                                    # 5 seconds in terms of 60 frames per second
                            # except Exception as e:
                            #     print(e)

                            if prevPlayer == currPlayer:
                                if currPlayer in nameRange:
                                    nameRange[currPlayer].append(frame_count)
                                else:
                                    nameRange[currPlayer] = [frame_count]
                                print(currPlayer)
                                print(nameRange[currPlayer])
                            else:
                                if clipFound:
                                    if len(nameRange) > 4
                                        clip_range = [nameRange[prevPlayer][0], nameRange[prevPlayer][-1]]
                                        nameRange[prevPlayer] = []
                                        print("taking temp clip out for release")
                                        clips["Players"].append({"player": temp_clips[0]["player"], "clip_url": f"https://www.youtube.com/embed/{grab.id}?&start={clip_range[0]//60}&end={clip_range[1]//60}", "date": grab.date})

                                    temp_clips = []
                                    clipFound = False

                        else:
                            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + intro_skip)
                            frame_count += intro_skip
                            continue
                    else:
                        if len(colors) == 0 :
                            inGame = grab.inGame(frame)
                            # print(inGame)
                            if inGame:
                                colors = grabTeamColors(frame)
                                print("Found colors: ", colors)
                                grab.setBounds(colors)
                            else:
                                # print("fast-forwarding to color: ", frame_count)
                                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + intro_skip)
                                frame_count += intro_skip
                                continue

                    frame_count += 1
                    prevPlayer = currPlayer
                else:
                    if clipFound:
                        if len(nameRange) > 4
                            clip_range = [nameRange[prevPlayer][0], nameRange[prevPlayer][-1]]
                            nameRange[prevPlayer] = []
                            print("taking temp clip out for release")
                            clips["Players"].append({"player": temp_clips[0]["player"], "clip_url": f"https://www.youtube.com/embed/{grab.id}?&start={clip_range[0]//60}&end={clip_range[1]//60}", "date": grab.date})

                        temp_clips = []
                        clipFound = False
                    break

            with open("../data/processed/completed.txt", "a+") as f:
                f.write(video[0])
            f.close()

            print("Finished video:", video[0])
            print(clips)

            for clip in clips["Players"]:
                if playerCol.find_one({"player": clip["player"]}) == None:
                    print("creating a new document")
                    playerCol.insert_one({
                        "player": clip["player"].split()[1],
                        "team": clip["player"].split()[0],
                        "clips": [{
                            "url": clip["clip_url"],
                            "date": clip["date"],
                        }]
                    })
                else:
                    print("appending clip to existing document")
                    playerCol.update_one(
                        {"player": clip["player"]},
                        {
                            "$push":
                            {
                                "clips": {
                                    "url": clip["clip_url"],
                                    "date": clip["date"],
                                    }
                                    # sort values by datetime value
                                    # figure out how to use $sort with datetime
                            }
                        }
                    )

            clips = {"Players": []}

            os.remove(f"videos/{video[0]}.mp4")


    os.remove(f"../data/playlist/{timestamp}.json")
    print("All data processed")

if __name__ == "__main__":
    main()
