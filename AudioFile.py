
from pydub import AudioSegment
from pydub.playback import play
import os
import utils


class audiofile:
    

    def __init__(self, file):
        """ Init audio stream """ 
        self.file = file

    def play(self):
        """ Play entire file """
        utils.displayInfoMessage('Playing Audio')
        if self.file[len(self.file) - 4:] == ".mp3":
            song = AudioSegment.from_mp3(self.file)
            play(song)
        elif self.file[len(self.file) - 4:] == ".wav":
            song = AudioSegment.from_wav(self.file)
            play(song)
        utils.displayInfoMessage('')

    def length(self):
        if self.file[len(self.file) - 4:] == ".mp3":
            song = AudioSegment.from_mp3(self.file)
            return song.duration_seconds
        elif self.file[len(self.file) - 4:] == ".wav":
            song = AudioSegment.from_wav(self.file)
            return song.duration_seconds