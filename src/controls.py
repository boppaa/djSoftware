from pynput import keyboard

def handle_key_release(player, key):
    try:
        if key.char == "f":
            player.toggle_playback(1)
            print(f"Deck 1 {'Playing' if player.playing1 else 'Paused'}")
        elif key.char == "j":
            player.toggle_playback(2)
            print(f"Deck 2 {'Playing' if player.playing2 else 'Paused'}")
        elif key.char == "g":
            player.crossfader_pos = max(0.0, player.crossfader_pos - 0.1)
            print(f"Crossfader: {player.crossfader_pos:.1f}")
        elif key.char == "h":
            player.crossfader_pos = min(1.0, player.crossfader_pos + 0.1)
            print(f"Crossfader: {player.crossfader_pos:.1f}")
        elif key.char == "c":
            player.volume1 = max(0.0, player.volume1 - 0.1)
            print(f"Deck 1 Volume: {player.volume1:.1f}")
    except AttributeError:
        pass

def listen_for_keys(player):
    try:
        with keyboard.Listener(on_release=lambda key: handle_key_release(player, key)) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\nClosing...")
