# SimpleRadioScheduler

Made as a quick, simple, and free way to get your radio station on air with features such as interval signals! (Gotta have those to make the station sound official! :3)

### Table of contents
[Getting started](#getting_started)
<br>
[More info](#more_info)

<br>

## Getting started
To configure the music sources and schedule for your station, use the `musicPaths` object in **config.json** to specify the paths/folders that your music files are in. This program is set up in a way that makes it easy to schedule different categories of music for different times.
<br>
You make each category a folder containing music that you decide is associated with that category. To schedule the categories, just make an object with a 24-hour timestamp of the time you want the radio station to switch to the specified category, and the category's folder path. **ALWAYS PUT A SLASH (/) AFTER A FILE PATH!**
<br>

Example:

```
"musicPaths": {
    "6:00": "Music/Morning_Ease/",
    "9:00": "Music/Daytime_Jams/",
    "18:30": "Music/Evening",
    "23:00": "Music/Night_Shift_Jazz"
}
```
<br>

To specify the path of your interval signal audio files, put it in the `intervalSignals` object. **ALWAYS PUT A SLASH (/) AFTER A FILE PATH!** If there is more than one file, the program will randomly select a file to play.
<br>
To specify the amount of songs that are played before your station's interval signal is played, set the `defaultSongGrouping` object.

<br>

To run it, just run `pip install -r requirements.txt` and then `python3 main.py`.
<br>
Happy broadcasting! :3

<br>

## More info
Whenever you update the configuration file while the program is running, your changes take effect when the next song starts playing.