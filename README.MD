Speech Shadowing App
=================

## Table of Contents
1. [Intro](#intro)
2. [Installation Instructions](#install)
3. [How-to](#how)
    1. [Upload Target Audio](#uploadtargetaudio)
    2. [Practice Speech Shadowing](#practicespeechshadowing)
    3. [Delete Target Audio](#deletetargetaudio)
    4. [Split Target Audio on silences](#splittargetaudio)
    5. [Hotkeys](#hotkeys)
4. [Tech Notes](#technotes)
    1. [Linux Installation](#linuxinstall)
    2. [Generating Single-File Executables](#singlefileexecutable)
    3. [Linux Single-File Executables](#linuxsinglefileexecutable)

Intro <a name="intro"></a>
------------
A python-based GUI app for practicing speech shadowing. Speech shadowing is a language learning method that has you listen to native speakers, then repeat what they say, and compare. This lets you practice things like: pronunciation, accent, pitch, and generally get more used to speaking your target language.

This app keeps things simple. You can upload "Target Audio" (the audio with a native speaker), select the audio you want from the list, play it, record yourself saying it, and then play back the native speaker and your version back-to-back, for comparison. 

The one extra feature that can be nice is that it also has a "Split on Silence" feature. This can take longer audio (e.g. a podcast in the target language), and split it down into individual sentences or phrases, based on silence in the audio. It's certainly not perfect, and if you want exact splits of audio, I'd suggest manually splitting it using audacity or other audio-manipulation programs. However, it can help create "basically correct" splits, and is nice as a first-try splitting the audio.

The audio is stored in two separate files, inside the same directory that the program is running in. One is called "TargetAudio", and one is called "RecordedAudio". 

Installation instructions <a name="install"></a>
------------
In the allbuilds folder, there are separate folders for each operating system. Look for your operating sytem version, and open that folder. There you will find a SpeechShadowApp executable and a README.MD file (a copy of this one). Download both and place where you want. Double click the SpeechShadowApp to run it on your computer.

If there is not a folder that matches your operating system in the allbuilds folder, that means I have not tested the app on your system yet. Instead follow the instructions under "Tech Notes"

How-to <a name="how"></a>
------------

### Upload Target Audio <a name="uploadtargetaudio"></a>
Go to File->"Upload Target Audio" and navigate in your filesystem to where you have the audio. You can select multiple audio files at once. Currently this program works with MP3 and WAV audio formats.

If you want, you can also upload target audio by manually copying MP3 or WAV files directly into the "TargetAudio" folder that is created in the same directory that the program is running in. The "Target Audio List" will not update until the next time you restart the program, however.

### Practice Speech Shadowing <a name="practicespeechshadowing"></a>
The "Target Audio List" displays all target audio you currently have uploaded. Click on the target audio you want to practice, then click "Play Target Audio" to playback the audio. Play it as many times as you want. When you want to record yourself, click "Start/Stop Recording", say the phrase or sentence, then click "Start/Stop Recording" again. To compare yourself with the target audio, click "Play Both Audio". It will then play the target audio, followed by your recorded audio.
Repeat this process until you sound the same, then move on to another target audio selection.

### Delete Target Audio <a name="deletetargetaudio"></a>
To delete a target audio, select it in the "Target Audio List". Then go to File->"Delete Selected Target Audio". There is no confirmation pop-up, it will simply delete it, so be sure you select the correct target audio to delete.

### Split Target Audio on silences <a name="splittargetaudio"></a>
If you have a longer audio that you want to split into individual sentences or phrases, you can try splitting the audio on silences. Select the target audio from the "Target Audio List", then go to File->"Split Target Audio On Silences". This can take a while for longer audio (really anything over a couple minutes will take a while), so be patient. 

The code assumes anything under -36dB is "silence", and requires the silence to be 1 second long in order to split the audio at that point. 

It will generate audio files in the target audio list area with the format: [original target audio filename]-auto-chunk\[number].mp3

### Hotkeys <a name="hotkeys"></a>
* Start/Stop recording - Space bar
* Listen to target audio - Enter
* Navigate Target Audio List - Up/Down arrow keys
* Listen to target and recorded audio - Right Ctrl key


Tech Notes <a name="technotes"></a>
------------

### Linux Installation <a name="linuxinstall"></a>
You'll need [ffmpeg](http://www.ffmpeg.org/) on your computer, as well as [python3](https://www.python.org/downloads/). Clone the repo either by using `git`, or download a zip and unzip on your machine. Open a bash terminal, navigate to where you unzipped the files, and run the code by typing `python3 main.py`

### Generating Single-File Executables <a name="singlefileexecutable"></a>
To generate a single-file executable, make sure you have pyinstaller on your machine (if you have pip, `pip3 install pyinstaller` should work), download this repo, and then type the following command:
```pyinstaller -n SpeechShadowApp main.py```

This will create a folder /dist/SpeechShadowApp that contains an executable called SpeechShadowApp.

#### Linux Single-File Executables <a name="linuxsinglefileexecutable"></a>
If you run a linux machine, you can run the `publishLinux.sh` script to generate a build for your version of Linux. First make sure the pyinstaller is on your computer, then:
1. Clone repo
2. Inside the cloned repo, type open a console and run `chomd +x ./publishLinux.sh` to make the file executable
3. Run the script `./publishLinux.sh`
4. inside the allbuilds folder you should find a folder with your Linux version on it, open it and the SpeechShadowApp executable will be there. If you don't know what version of linux you have, run `lsb_release -ds`
