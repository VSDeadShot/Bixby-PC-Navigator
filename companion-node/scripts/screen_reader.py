import time
import json
import urllib.request
import urllib.error
import sys

# Try to import required packages, if missing, tell the user gracefully
try:
    import pyperclip
    import pyautogui
except ImportError:
    print("Missing dependencies. Run: pip install pyautogui pyperclip")
    sys.exit(1)

import os
api_key = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

print("Switch to the window you want to summarize! You have 3 seconds...")
time.sleep(3)

def get_screen_text():
    # Save the current clipboard so we don't overwrite the user's copied items
    old_clipboard = pyperclip.paste()
    
    # Click to ensure the window is active (optional, but helps)
    # pyautogui.click()
    
    # Simulate Ctrl+A (Select All) and Ctrl+C (Copy)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    
    # Grab the text we just copied
    copied_text = pyperclip.paste()
    
    # Restore the user's original clipboard
    pyperclip.copy(old_clipboard)
    
    # De-select text by pressing right arrow
    pyautogui.press('right')
    
    return copied_text

def summarize_text(text):
    if not text or len(text.strip()) == 0:
        return "There doesn't seem to be any readable text on the active screen."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Truncate text to the first 15,000 characters so we don't overload the prompt
    truncated_text = text[:15000]
    
    prompt = "You are Bixby, a helpful AI PC assistant. Please summarize the following text currently open on the user's screen in 2 to 3 conversational sentences so it can be read out loud easily: \n\n" + truncated_text
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        return "I had trouble analyzing the screen."

text = get_screen_text()
summary = summarize_text(text)
print(summary)
