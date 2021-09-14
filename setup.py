import os

os.system("youtube-dl --flat-playlist PLisfUdjySbZVoTRbAlfObs8dI-cb-gWk- > playlist.txt")

num_videos = ""

with open("playlist.txt", "r") as f:
    for i, line in enumerate(f):
        if i == 3:
            num_videos = line.split()[-1]
            break

print("Videos in playlist: ", num_videos)
