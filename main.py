# Copyright McTechDev/Mr_McTech AKA YourFurryDeveloper on GitHub 2026

# Audio device is your OSe's default audio device
from just_playback import Playback
import json
import os
import random
import time
from datetime import datetime

global config
global musicPaths
global intervalsPath
global songsBeforeInterval
global pauseTimeSecs

def updateConfig():
    global config
    global musicPaths
    global intervalsPath
    global songsBeforeInterval
    global pauseTimeSecs
    
    config = json.load(open("config.json", "r"))
    musicPaths = config["musicPaths"] # Music path MUST end with a slash (/)
    intervalsPath = config["intervalSignals"] # Interval signal path MUST end with a slash (/)
    songsBeforeInterval = config["defaultSongGrouping"]
    pauseTimeSecs = config["pauseTimeSecs"]

if not os.name == "nt":
    os.system("clear")
else:
    os.system("cls")

#print("Audio devices:")
#print(sd.query_devices())
#device_id = int(input("Select audio device > "))
#sd.default.device = device_id

updateConfig()

global player
player = Playback()

playedSongs = []
numPlayedSongs = songsBeforeInterval
totalSongsPlayed = 0
curMusicPath = ""

playedIntervals = []
totalIntervalsPlayed = 0
curIntervalPath = ""

def playRandomFile(audioFilePaths, totalFilesPlayed, playedFiles, curFilePath):
    global player

    for c in range(len(audioFilePaths)):
        #c = len(audioFilePaths) - (c + 1)
        audioFilePathsList = list(audioFilePaths)
        audioFilePathsList.reverse()
        
        curTime = datetime.now().time()
        #categoryTime = list(audioFilePaths)[c]
        categoryTime = audioFilePathsList[c]
        categoryTime = datetime.strptime(categoryTime, "%H:%M").time()
        
        musicPath = audioFilePaths[audioFilePathsList[c]]
        if curTime >= categoryTime and not musicPath == curFilePath:
            print(f"\nSwitching audio source to {musicPath} (Scheduled for {audioFilePathsList[c]})\n")
            curFilePath = musicPath
            playedFiles = []
            break
    
    songList = os.listdir(musicPath)
    supportedFormats = [".mp3", ".wav", ".flac", ".ogg"]
    songList = [s for s in songList if str(os.path.splitext(s)[1]).lower() in supportedFormats]
    
    if len(playedFiles) == len(songList):
        playedFiles = []
        totalFilesPlayed = 0
    else:
        totalFilesPlayed += 1
    
    curSong = random.choice(songList)
    while curSong in playedFiles:
        curSong = random.choice(songList)
    playedFiles.append(curSong)
    
    print(f"Current audio file: {curSong}")
    player.load_file(musicPath + curSong)
    total_time = time.strftime('%H:%M:%S', time.gmtime(player.duration))
    player.play()
    
    while player.active:
        curSongTime = time.strftime('%H:%M:%S', time.gmtime(player.curr_pos))
        print(f"\033[K[{curSongTime}/{total_time}]", end="\r", flush=True)
    
    return playedFiles, totalFilesPlayed, curFilePath


print("=| SimpleRadioScheduler by Mr_McTech/McTechDev AKA YourFurryDeveloper on GitHub :3 |=")

print("\nCONFIGURATION")
print("================================================")
for setting in range(len(config)):
    curSetting = list(config)[setting]
    print(f"{list(config)[setting]}: {config[curSetting]}")
print("================================================\n")
print("Config loaded and updated. Config can be updated during playback, and will take effect once the next audio starts.\nStarting song rotation.\n")

print("================================================\n")

time.sleep(2)

while True:
    updateConfig()
    
    if numPlayedSongs == songsBeforeInterval:
        playedIntervals, totalIntervalsPlayed, curIntervalPath = playRandomFile(intervalsPath, totalIntervalsPlayed, playedIntervals, curIntervalPath)
        numPlayedSongs = 0
        time.sleep(pauseTimeSecs)
    
    playedSongs, totalSongsPlayed, curMusicPath = playRandomFile(musicPaths, totalSongsPlayed, playedSongs, curMusicPath)
    
    numPlayedSongs += 1
    time.sleep(pauseTimeSecs)