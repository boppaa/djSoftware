import numpy as np
import sounddevice as sd

class AudioPlayer:
    def __init__(self, track1, track2, sample_rate):
        self.original_track1 = track1
        self.original_track2 = track2
        self.track1 = track1
        self.track2 = track2
        self.sample_rate = sample_rate
        self.bpm1 = None
        self.bpm2 = None
        self.tempo_factor1 = 1.0
        self.tempo_factor2 = 1.0
        self.pos1, self.pos2 = 0, 0
        self.playing1, self.playing2 = False, False
        self.volume1, self.volume2 = 1.0, 1.0
        self.crossfader_pos = 0.5

    def callback(self, outdata, frames, time, status):
        buffer = np.zeros((frames, 2), dtype=np.float32)
        crossfade1, crossfade2 = 1.0 - self.crossfader_pos, self.crossfader_pos

        if self.playing1 and self.pos1 < len(self.track1):
            output1 = self.track1[self.pos1:self.pos1+frames] * self.volume1 * crossfade1
            buffer[:len(output1)] += output1
            self.pos1 += frames

        if self.playing2 and self.pos2 < len(self.track2):
            output2 = self.track2[self.pos2:self.pos2+frames] * self.volume2 * crossfade2
            buffer[:len(output2)] += output2
            self.pos2 += frames

        outdata[:] = buffer

    def toggle_playback(self, deck):
        if deck == 1:
            self.playing1 = not self.playing1
        elif deck == 2:
            self.playing2 = not self.playing2
    
