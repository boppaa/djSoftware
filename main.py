import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from pynput import keyboard
import librosa
import librosa.display

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

# Global variables for tracking playback state
pos1, pos2 = 0, 0
playing1, playing2 = False, False
volume1, volume2 = 1.0, 1.0  # Default volume (100%)
crossfader_pos = 0.5
tempo1, tempo2 = 120.0, 120.0

# Load two MP3 tracks
track1_array, SAMPLE_RATE = load_track("brown.mp3")
track2_array, _ = load_track("leon.mp3")
print("test1")
tempo1 = detect_bpm("brown.mp3")
print("test2")
tempo2 = detect_bpm("leon.mp3")

print("test 3")

print(f"Detected BPM - Track 1: {tempo1:.2f}, Track 2: {tempo2:.2f}")

# Audio callback function
def callback(outdata, frames, time, status):
    global pos1, pos2
    if status:
        print(status)

    buffer = np.zeros((frames, 2), dtype=np.float32)  # Stereo buffer

    # Corrected Crossfader Logic (Smooth Transition)
    crossfade1 = 1.0 - crossfader_pos  # Deck 1 fades out as crossfader_pos increases
    crossfade2 = crossfader_pos  # Deck 2 fades in as crossfader_pos increases

    if playing1 and pos1 < len(track1_array):
        output1 = track1_array[pos1:pos1+frames] * volume1 * crossfade1
        output1 = output1[:frames]  # Ensure length is correct
        buffer[:len(output1)] += output1
        pos1 += frames

    if playing2 and pos2 < len(track2_array):
        output2 = track2_array[pos2:pos2+frames] * volume2 * crossfade2
        output2 = output2[:frames]  # Ensure length is correct
        buffer[:len(output2)] += output2
        pos2 += frames

    outdata[:] = buffer  # Send audio to output


# Function to toggle play/pause on key release
def on_key_release(key):
    global playing1, playing2, volume1, volume2, crossfader_pos
    try:
        if key.char == "f":
            playing1 = not playing1
            print(f"Deck 1 {'Playing' if playing1 else 'Paused'}")
        elif key.char == "j":
            playing2 = not playing2
            print(f"Deck 2 {'Playing' if playing2 else 'Paused'}")
        elif key.char == "c":
            volume1 = max(0.0, volume1 - 0.1)  # Decrease volume but not below 0
            print(f"Deck 1 Volume: {volume1:.1f}")
        elif key.char == "v":
            volume1 = min(volume1 + 0.1, 1.0)  # Decrease volume but not below 0
            print(f"Deck 1 Volume: {volume1:.1f}")
        elif key.char == "n":
            volume2 = max(0.0, volume2 - 0.1)  # Decrease volume but not below 0
            print(f"Deck 2 Volume: {volume2:.1f}")
        elif key.char == "m":
            volume2 = min(volume2 + 0.1, 1.0)  # Decrease volume but not below 0
            print(f"Deck 2 Volume: {volume2:.1f}")    
        elif key.char == "g":
            crossfader_pos = max(0.0, crossfader_pos - 0.1)  # Move toward Deck 1
            print(f"Crossfader: {crossfader_pos:.1f}")
        elif key.char == "h":
            crossfader_pos = min(1.0, crossfader_pos + 0.1)  # Move toward Deck 2
            print(f"Crossfader: {crossfader_pos:.1f}")
        elif key.char == "d":
            tempo1 += 1.0  # Increase Deck 1 tempo
            print(f"Deck 1 Tempo: {tempo1:.1f} BPM")
        elif key.char == "s":
            tempo1 -= 1.0  # Decrease Deck 1 tempo
            print(f"Deck 1 Tempo: {tempo1:.1f} BPM")
        elif key.char == "l":
            tempo2 += 1.0  # Increase Deck 2 tempo
            print(f"Deck 2 Tempo: {tempo2:.1f} BPM")
        elif key.char == "k":
            tempo2 -= 1.0  # Decrease Deck 2 tempo
            print(f"Deck 2 Tempo: {tempo2:.1f} BPM")

    except AttributeError:
        pass  # Ignore special keys

# Start streaming audio
with sd.OutputStream(samplerate=SAMPLE_RATE, channels=2, callback=callback):
    print("Press 'f' or 'j' to toggle playback (release the key to toggle).")

    # Start listening for key events
    try:
        with keyboard.Listener(on_release=on_key_release) as listener:
            listener.join()  # Keeps the program running
    except KeyboardInterrupt:
        print("\nClosing...")
