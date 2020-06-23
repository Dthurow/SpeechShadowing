# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
# code taken from https://stackoverflow.com/a/46001755 and modified for use here
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import os
import utils


class AudioSplitter(object):

    def __init__(self, filedirectory, filename, minsilencelen=1000, silencethresh=-36):
        self.filedirectory = filedirectory
        self.filename = filename
        self.minsilencelen = minsilencelen
        self.silencethresh = silencethresh
        self.silencepaddinglen = 500

    # Define a function to normalize a chunk to a target amplitude.
    def match_target_amplitude(self, aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    def split(self):
        utils.displayInfoMessage("Starting Split")
        # Load your audio.
        song = AudioSegment.from_mp3(os.path.join(self.filedirectory, self.filename))

        # Split track where the silence is the min silence length or more and get chunks using 
        # the imported function.
        chunks = split_on_silence (
            # Use the loaded audio.
            song, 
            # Specify that a silent chunk must be at least minsilencelen long, in milliseconds
            min_silence_len = self.minsilencelen,
            # Consider a chunk silent if it's quieter than the silence threshhold dBFS.
            # (You may want to adjust this parameter.)
            silence_thresh = self.silencethresh,
            keep_silence=300,
            seek_step=250
        )
        
        numwidth = len(str(len(chunks)))
        # Process each chunk with your parameters
        for i, chunk in enumerate(chunks):
            # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
            silence_chunk = AudioSegment.silent(duration=self.silencepaddinglen)

            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunk + silence_chunk

            # Normalize the entire chunk.
            normalized_chunk = self.match_target_amplitude(audio_chunk, -20.0)

            # Export the audio chunk with new bitrate.
            utils.displayInfoMessage("Exporting {0}-auto-chunk{1}.mp3.".format(self.filename[0:len(self.filename)-4], str(i).zfill(numwidth)))
            normalized_chunk.export(
                self.filedirectory + "//{0}-auto-chunk{1}.mp3".format(self.filename[0:len(self.filename)-4], str(i).zfill(numwidth)),
                bitrate = "192k",
                format = "mp3"
            )
            utils.displayInfoMessage("Splitting Complete!")