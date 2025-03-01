import numpy as np
from pydub import AudioSegment
import librosa

# Load and preprocess audio files
def load_track(file):
    track = AudioSegment.from_file(file)
    track = track.set_channels(2).set_frame_rate(44100)  # Ensure stereo, standard sample rate
    track_array = np.array(track.get_array_of_samples(), dtype=np.float32)
    track_array = track_array.reshape(-1, 2)  # Convert to stereo (N, 2)
    track_array /= np.iinfo(np.int16).max  # Normalize to -1 to 1
    return track_array, track.frame_rate

def detect_bpm(file):
    y, sr = librosa.load(file, sr=44100)  # Load audio with standard sample rate
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)  # Detect onset envelope
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)  # Estimate tempo
    return float(tempo.item())  # Return detected BPM