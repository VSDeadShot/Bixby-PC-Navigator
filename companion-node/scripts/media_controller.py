import sys
import ctypes
import time

# Virtual Key Codes for Windows Media Controls
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

def press_key(hexKeyCode):
    """Simulates a key press and release."""
    # Press
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0, 0)
    time.sleep(0.05)
    # Release
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, 2, 0)

def main():
    if len(sys.argv) < 2:
        print("Usage: python media_controller.py <command>")
        print("Commands: playpause, next, prev, volup, voldown, mute")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == "playpause":
        press_key(VK_MEDIA_PLAY_PAUSE)
        print("Toggled Play/Pause")
    elif command == "next":
        press_key(VK_MEDIA_NEXT_TRACK)
        print("Skipped to Next Track")
    elif command == "prev":
        press_key(VK_MEDIA_PREV_TRACK)
        print("Went to Previous Track")
    elif command == "volup":
        # Press a few times for noticeable volume change
        for _ in range(5):
            press_key(VK_VOLUME_UP)
        print("Increased Volume")
    elif command == "voldown":
        for _ in range(5):
            press_key(VK_VOLUME_DOWN)
        print("Decreased Volume")
    elif command == "mute":
        press_key(VK_VOLUME_MUTE)
        print("Toggled Mute")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
