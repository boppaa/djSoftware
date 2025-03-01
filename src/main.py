from audio_processing import load_track, detect_bpm
from playback import AudioPlayer
from controls import listen_for_keys
import sounddevice as sd

# Load tracks
track1, SAMPLE_RATE = load_track("../mp3Files/brown.mp3")
track2, _ = load_track("../mp3Files/leon.mp3")

# Detect BPM
tempo1 = detect_bpm("../mp3Files/brown.mp3")
tempo2 = detect_bpm("../mp3Files/leon.mp3")
print(f"Detected BPM - Track 1: {tempo1:.2f}, Track 2: {tempo2:.2f}")

# Initialize player
player = AudioPlayer(track1, track2, SAMPLE_RATE)

# Start audio stream
with sd.OutputStream(samplerate=SAMPLE_RATE, channels=2, callback=player.callback):
    print("Press 'f' or 'j' to toggle playback.")
    listen_for_keys(player)
