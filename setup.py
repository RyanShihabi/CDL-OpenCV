import os
import json
import datetime

timestamp = str(datetime.datetime.now())[:10]

os.system(f"youtube-dl --dump-single-json PLisfUdjySbZVoTRbAlfObs8dI-cb-gWk- > {timestamp}.json")

#iterate through videos depending on what the playlist requirements provide

# for i in range(num_videos+1):
#     os.system("youtube-dl --flat-playlist PLisfUdjySbZVoTRbAlfObs8dI-cb-gWk- > playlist.txt")
