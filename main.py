# Copyright McTechDev/Mr_McTech AKA YourFurryDeveloper on GitHub 2026

# Audio device is your OSe's default audio device
from just_playback import Playback
import json
import os
import random
import time
from datetime import datetime
import sounddevice as sd

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

player = Playback()

print("=| SimpleRadioScheduler by Mr_McTech/McTechDev AKA YourFurryDeveloper on GitHub :3 |=")

updateConfig()
print("\nCONFIGURATION")
print("================================================")
for setting in range(len(config)):
    curSetting = list(config)[setting]
    print(f"{list(config)[setting]}: {config[curSetting]}")
print("================================================\n")
print("Config loaded and updated. Config can be updated during playback, and will take effect once the next audio starts.\nStarting song rotation.\n")

time.sleep(2)

playedSongs = []
numPlayedSongs = songsBeforeInterval
totalSongsPlayed = 0
curMusicPath = ""
while True:
    updateConfig()
    
    if numPlayedSongs == songsBeforeInterval:
        songList = os.listdir(intervalsPath)
        supportedFormats = [".mp3", ".wav", ".flac", ".ogg"]
        songList = [s for s in songList if str(os.path.splitext(s)[1]).lower() in supportedFormats]
        
        curSong = random.choice(songList)
        while curSong in playedSongs:
            curSong = random.choice(songList)
        
        print(f"Current interval signal file: {curSong}")
        player.load_file(intervalsPath + curSong)
        total_time = time.strftime('%H:%M:%S', time.gmtime(player.duration))
        player.play()
        
        while player.active:
            curSongTime = time.strftime('%H:%M:%S', time.gmtime(player.curr_pos))
            print(f"\033[K[{curSongTime}/{total_time}]", end="\r", flush=True)
    numPlayedSongs = 0
    time.sleep(pauseTimeSecs)
    
    for c in range(len(musicPaths)):
        c = len(musicPaths) - (c + 1)
        
        curTime = datetime.now().time()
        categoryTime = list(musicPaths)[c]
        categoryTime = datetime.strptime(categoryTime, "%H:%M").time()
        
        musicPath = musicPaths[list(musicPaths)[c]]
        if curTime >= categoryTime and not musicPath == curMusicPath:
            print(f"\nSwitching music source to {musicPath} (Scheduled for {list(musicPaths)[c]})\n")
            curMusicPath = musicPath
            playedSongs = []
            break
        else:
            break
    
    songList = os.listdir(musicPath)
    supportedFormats = [".mp3", ".wav", ".flac", ".ogg"]
    songList = [s for s in songList if str(os.path.splitext(s)[1]).lower() in supportedFormats]
    
    if totalSongsPlayed == len(songList):
        playedSongs = []
    
    curSong = random.choice(songList)
    while curSong in playedSongs:
        curSong = random.choice(songList)
    playedSongs.append(curSong)
    
    print(f"Current song file: {curSong}")
    player.load_file(musicPath + curSong)
    total_time = time.strftime('%H:%M:%S', time.gmtime(player.duration))
    player.play()
    
    while player.active:
        curSongTime = time.strftime('%H:%M:%S', time.gmtime(player.curr_pos))
        print(f"\033[K[{curSongTime}/{total_time}]", end="\r", flush=True)
    
    numPlayedSongs += 1
    totalSongsPlayed += 1
    time.sleep(pauseTimeSecs)