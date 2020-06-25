import tkinter as tk
from tkinter import filedialog
import recorder
import AudioFile
import audioSplitter
import os
import time
from os.path import join, getsize
import math
import shutil
import webbrowser
import markdown
import utils

# --- global values ---
targetAudioFolder = "./TargetAudio"
recordedAudioFolder = "./RecordedAudio"
silenceThreshold = -36


# --- functions ---

# -- helper functions

def getTargetAudioFileName():
    selectedTuple = targetAudioListBox.curselection()
    if (len(selectedTuple) > 0):
        filename = targetAudioListBox.get(selectedTuple[0])
        filename = filename[0:filename.rfind(" - ")]
        return filename
    else:
        print("selectedTuple is not greater than 0")
        return ''

def getRecordedAudioFileName():
    targetFilename = getTargetAudioFileName()
    if targetFilename != '':
        filename = "recordedAudio-" + targetFilename[0:len(targetFilename)-4] + ".wav"
        return filename
    else:
        print("targetfilename doesn't exist")
        return ''

def refreshTargetAudioList():
    global running
    if running is not None:
        utils.displayErrorMessage('recording audio, gotta stop that first')
    else:
        # remove all elements in targetAudioListbox
        targetAudioListBox.delete(0, targetAudioListBox.size())
        #loop thru files
        fileList = os.listdir(targetAudioFolder)
        fileList.sort()
        for file in fileList:
            if file[len(file) - 4:] in [".wav", ".mp3"]:
                displayname = file
                audioFile = AudioFile.audiofile(os.path.join(targetAudioFolder, file))
                length = audioFile.length()
                displaylength = ""
                if length > 60:
                    displaylength = str(math.floor(length/60)) + ":" + str(math.floor(length % 60)).zfill(2)
                else:
                    displaylength = str(math.floor(length % 60)) + " seconds"
                displayname += " - " + displaylength
                targetAudioListBox.insert("end", displayname )
                targetAudioListBox.see(targetAudioListBox.size())
                utils.root.update()

def initialChecks():
    global running
    #general things to do before running events
    if running is not None:
        utils.displayErrorMessage('Recording Audio, Stop That First')
        return False
    utils.displayErrorMessage('')
    utils.displayInfoMessage('')
    return True

# -- event functions

def openHelp(event=None):
    if not os.path.exists("./README.html"):
        if os.path.exists("./README.MD"):
            markdown.markdownFromFile(input="./README.MD",output="./README.html")
        else:
            utils.displayErrorMessage("Cannot find help page")
            return
    webbrowser.open('./README.html')

# -- Target Audio Events --
def uploadTargetAudio(event=None):
    if initialChecks():
        filenames = filedialog.askopenfilenames(title="Select Target Audio", filetypes=[("Audio Files", ".mp3 .wav")])
        for filename in filenames:
            shutil.copy(filename, targetAudioFolder)
        refreshTargetAudioList()

def deleteTargetAudio(event=None):
    # remove all elements in targetAudioListbox
    if initialChecks():
        filename = getTargetAudioFileName()
        os.remove(os.path.join(targetAudioFolder, filename))
        refreshTargetAudioList()

def splitTargetAudio(event=None):
    global silenceThreshold
    if initialChecks():
        filename = getTargetAudioFileName()
        if filename != '':
            audiosplit = audioSplitter.AudioSplitter(targetAudioFolder, filename, silencethresh=silenceThreshold)
            audiosplit.split()
            refreshTargetAudioList()
        else:
            utils.displayErrorMessage('Select Target Audio To Split')

def playtargetaudio(event=None):
    if initialChecks():
        filename = getTargetAudioFileName()
        if filename != '':
            a = AudioFile.audiofile(os.path.join(targetAudioFolder, filename))
            a.play()
        else:
            utils.displayErrorMessage("Select Target Audio First")


# -- Recorded Audio Events --
def playrecordedaudio(event=None):
    if initialChecks():
        filename = getRecordedAudioFileName()
        if filename != '':
            if os.path.exists(os.path.join(recordedAudioFolder, filename)):
                print("playing " + os.path.join(recordedAudioFolder, filename))
                a = AudioFile.audiofile(os.path.join(recordedAudioFolder, filename))
                a.play()
            else:
                utils.displayErrorMessage("You must record audio first")
        else:
            utils.displayErrorMessage("You must record audio first")

def playbothaudio(event=None):
   if initialChecks():
        playtargetaudio()
        playrecordedaudio()


def startRecording(event=None):
    global running
    if initialChecks():
        filename = getRecordedAudioFileName()
        if filename != '':
            running = rec.open(os.path.join(recordedAudioFolder,filename), 'wb')
            running.start_recording()
        else:
            utils.displayErrorMessage("Select Target Audio First")

def stopRecording(event=None):
    global running

    if running is not None:
        running.stop_recording()
        running.close()
        running = None
    else:
        utils.displayErrorMessage('Recording Not Running')

def startStopRecording(event=None):
    global running
    if running is not None:
        stopRecording()
    else:
        startRecording()


def displayHotkeysPopup(event=None):
    hotkeyList="""
    Start/Stop recording - Space bar
    Listen to target audio - Enter
    Navigate Target Audio List - Up/Down arrow keys
    Listen to target and recorded audio - Right Ctrl key
    """
    popupWindow = tk.Toplevel(utils.root)
    popupWindow.wm_geometry("750x300")
    popupWindow.title("Hotkey list")
    msg = tk.Message(popupWindow, text=hotkeyList, width=750)
    msg.pack()

    button = tk.Button(popupWindow, text="Ok", command=popupWindow.destroy)
    button.pack(pady=5)
    utils.root.wait_window(popupWindow)

def updateSilenceThreshhold(event=None):
    global silenceThreshold

    def silenceThreshholdClose():
        global silenceThreshold
        try:
            silenceThreshold = int(popupEntry.get())
            print(silenceThreshold)
            popupWindow.destroy()
        except:
            popupErrorMsg.set("Must be a valid number")


    popupWindow = tk.Toplevel(utils.root)
    popupWindow.wm_geometry("1000x250")
    popupWindow.title("Change Silence dBS")
    popupLabel = tk.Label(popupWindow, text="Update what 'silence' is defined as when splitting target audio (in dBS)")
    popupLabel.pack(pady=5)
    popupLabel2 = tk.Label(popupWindow, text="Current Silence Threshold is: " + str(silenceThreshold) + "dBS")
    popupLabel2.pack(pady=5)

    popupEntry = tk.Entry(popupWindow)
    popupEntry.pack()

    button = tk.Button(popupWindow, text="Update", command=silenceThreshholdClose)
    button.pack(pady=5)

    popupErrorMsg = tk.StringVar()
    popupError = tk.Label(popupWindow, textvariable=popupErrorMsg, fg="red")
    popupError.pack(pady=5)

    utils.root.wait_window(popupWindow)

# --- main ---

# create the target audio and recorded audio folders, if they don't already exist
if not os.path.exists(targetAudioFolder):
    os.makedirs(targetAudioFolder)
if not os.path.exists(recordedAudioFolder):
    os.makedirs(recordedAudioFolder)

rec = recorder.Recorder(channels=2)
running = None

utils.root = tk.Tk()
utils.root.title("Speech Shadowing App")

# -- create menu bar --
menubar = tk.Menu(utils.root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Upload Target Audio", command=uploadTargetAudio)
filemenu.add_command(label="Split Target Audio on Silences", command=splitTargetAudio)
filemenu.add_command(label="Delete Selected Target Audio", command=deleteTargetAudio)
filemenu.add_command(label="Update Silence Threshold", command=updateSilenceThreshhold)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=utils.root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=openHelp)
helpmenu.add_command(label="Hotkeys", command=displayHotkeysPopup)
menubar.add_cascade(label="Help", menu=helpmenu)

utils.root.config(menu=menubar)

# -- create info message area
utils.infoMessage = tk.StringVar(utils.root)
infomsg = tk.Label(utils.root, textvariable=utils.infoMessage, fg="blue")
infomsg.pack()

# -- create error message area
utils.errorMessage = tk.StringVar(utils.root)
error = tk.Label(utils.root, textvariable=utils.errorMessage, fg="red")
error.pack()

# -- generate list of target audio
targetAudioFrame = tk.Frame(utils.root)
targetAudioFrame.pack(pady=10)

label = tk.Label(targetAudioFrame, text="Target Audio List")
label.pack()

targetAudioListBoxFrame = tk.Frame(targetAudioFrame)
targetAudioListBoxFrame.pack(padx=10)

targetAudioListBox = tk.Listbox(targetAudioListBoxFrame, selectmode="SINGLE", width=75)


scrollbar = tk.Scrollbar(targetAudioListBoxFrame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y,pady=5)
targetAudioListBox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=targetAudioListBox.yview)

targetAudioListBox.pack(pady=5)


# --  create buttons
button_playtarget = tk.Button(utils.root, text='Play Target Audio (Enter Key)', command=playtargetaudio)
button_playtarget.pack(pady=5)


button_rec = tk.Button(utils.root, text='Start/Stop Recording (Space bar)', command=startStopRecording)
button_rec.pack(pady=5)

button_playboth = tk.Button(utils.root, text='Play Both Audio (Right Ctrl Key)', command=playbothaudio)
button_playboth.pack(pady=5)

# -- create keybindings
utils.root.bind("<Return>", playtargetaudio)
utils.root.bind("<Control_R>", playbothaudio)

def targetAudioSelectionDown(event=None):
    selectedTuple = targetAudioListBox.curselection()
    if (len(selectedTuple) > 0):
        i = selectedTuple[0]
        if (i < targetAudioListBox.size()):
            targetAudioListBox.selection_clear(i)
            targetAudioListBox.select_set(i+1)
            targetAudioListBox.see(i+1)
    else:
        targetAudioListBox.select_set(0)
        targetAudioListBox.see(0)

def targetAudioSelectionUp(event=None):
    selectedTuple = targetAudioListBox.curselection()
    if (len(selectedTuple) > 0):
        i = selectedTuple[0]
        if (i > 0):
            targetAudioListBox.selection_clear(i)
            targetAudioListBox.select_set(i-1)
            targetAudioListBox.see(i-1)

    else:
        targetAudioListBox.select_set(0)
        targetAudioListBox.see(0)

utils.root.bind("<Down>", targetAudioSelectionDown)
utils.root.bind("<Up>", targetAudioSelectionUp)
utils.root.bind("<space>", startStopRecording)


# -- load target audio initially. Set info message also has a bonus that it'll start
# the GUI before the targetAudio list has completed
utils.displayInfoMessage("Loading Target Audio...")
refreshTargetAudioList()
utils.displayInfoMessage("")

utils.root.mainloop() 
