"""
=============================================================================
             💖 TINA'S MAGIC LOVE TYPER 💖
   Simulates realistic, human-like live typing directly into any chat box!
   Works with WhatsApp Web/Desktop, Telegram, Instagram, Messages, etc.
=============================================================================
"""

import sys
import time
import random
import ctypes
from ctypes import wintypes

# Try importing winsound for Windows audio cues (built-in on Windows)
try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

# =============================================================================
# WINDOWS NATIVE UNICODE KEYBOARD SIMULATOR (ZERO DEPENDENCIES REQUIRED!)
# Supports all emojis (😊, 😏, ❤️, 🍦), accented characters, and Shift+Enter
# =============================================================================
user32 = ctypes.windll.user32

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
VK_SHIFT = 0x10
VK_RETURN = 0x0D

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_input", _INPUT),
    ]

def send_unicode_char(char):
    """Types any Unicode character or emoji using Windows native SendInput."""
    utf16_bytes = char.encode("utf-16le")
    for i in range(0, len(utf16_bytes), 2):
        code_unit = int.from_bytes(utf16_bytes[i:i+2], "little")
        
        # Key down
        input_down = INPUT(type=INPUT_KEYBOARD)
        input_down.ki = KEYBDINPUT(wVk=0, wScan=code_unit, dwFlags=KEYEVENTF_UNICODE, time=0, dwExtraInfo=0)
        user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(INPUT))
        
        # Key up
        input_up = INPUT(type=INPUT_KEYBOARD)
        input_up.ki = KEYBDINPUT(wVk=0, wScan=code_unit, dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, time=0, dwExtraInfo=0)
        user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(INPUT))

def send_shift_enter():
    """Simulates Shift + Enter (creates a new line without sending the message in chat apps)."""
    # Shift Down
    s_down = INPUT(type=INPUT_KEYBOARD)
    s_down.ki = KEYBDINPUT(wVk=VK_SHIFT, wScan=0, dwFlags=0, time=0, dwExtraInfo=0)
    
    # Enter Down
    e_down = INPUT(type=INPUT_KEYBOARD)
    e_down.ki = KEYBDINPUT(wVk=VK_RETURN, wScan=0, dwFlags=0, time=0, dwExtraInfo=0)
    
    # Enter Up
    e_up = INPUT(type=INPUT_KEYBOARD)
    e_up.ki = KEYBDINPUT(wVk=VK_RETURN, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0)
    
    # Shift Up
    s_up = INPUT(type=INPUT_KEYBOARD)
    s_up.ki = KEYBDINPUT(wVk=VK_SHIFT, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0)
    
    user32.SendInput(1, ctypes.byref(s_down), ctypes.sizeof(INPUT))
    time.sleep(0.04)
    user32.SendInput(1, ctypes.byref(e_down), ctypes.sizeof(INPUT))
    time.sleep(0.04)
    user32.SendInput(1, ctypes.byref(e_up), ctypes.sizeof(INPUT))
    time.sleep(0.04)
    user32.SendInput(1, ctypes.byref(s_up), ctypes.sizeof(INPUT))

def send_enter():
    """Presses Enter to send the message."""
    e_down = INPUT(type=INPUT_KEYBOARD)
    e_down.ki = KEYBDINPUT(wVk=VK_RETURN, wScan=0, dwFlags=0, time=0, dwExtraInfo=0)
    e_up = INPUT(type=INPUT_KEYBOARD)
    e_up.ki = KEYBDINPUT(wVk=VK_RETURN, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0)
    user32.SendInput(1, ctypes.byref(e_down), ctypes.sizeof(INPUT))
    time.sleep(0.05)
    user32.SendInput(1, ctypes.byref(e_up), ctypes.sizeof(INPUT))

def play_beep(freq, duration):
    """Plays audio tone if available."""
    if HAS_SOUND:
        try:
            winsound.Beep(freq, duration)
        except Exception:
            pass

# =============================================================================
# PRESET ROMANTIC MESSAGES
# =============================================================================
PRESET_MESSAGES = {
    "1": (
        "The Sweet Compliment (Original)",
        """Heyy Tina 😊
I was just thinking about you...
And I realized I never told you this
You honestly have the best smile I've seen in a while
Okay that's all. Don't blush too much 😏"""
    ),
    "2": (
        "The Ice Cream Date Invite",
        """Hey Tina 🍦
Quick question...
Are you free this week?
I was thinking we grab ice cream together... my treat 😉
What do you say? ✨"""
    ),
    "3": (
        "The Smooth & Flirty",
        """Hey Tina 😊
I was just thinking...
Life is short, ice cream is cold, and you're way too pretty to not go on a date with me this week 😏
Let me take you out for dessert! 🍨❤️"""
    )
}

def print_banner():
    banner = r"""
  ╔═══════════════════════════════════════════════════════════════════╗
  ║                                                                   ║
  ║      ♥ ♥ ♥   T I N A ' S   M A G I C   T Y P E R   ♥ ♥ ♥          ║
  ║                                                                   ║
  ║   Simulates realistic, human live typing into any chat box!       ║
  ║   Works with WhatsApp, Telegram, Instagram, iMessage, etc.        ║
  ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def choose_message():
    print("💌 Select a surprise message for Tina:\n")
    for key, (title, text) in PRESET_MESSAGES.items():
        first_line = text.split("\n")[0]
        print(f"  [{key}] {title}")
        print(f"      Preview: \"{first_line}...\"\n")
    print("  [4] Write Your Own Custom Message\n")

    choice = input("Enter your choice (1-4, default is 1): ").strip()
    if choice in PRESET_MESSAGES:
        return PRESET_MESSAGES[choice][1]
    elif choice == "4":
        print("\nEnter your custom message (Type/paste your text, then type END on a new line):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        custom_text = "\n".join(lines).strip()
        return custom_text if custom_text else PRESET_MESSAGES["1"][1]
    else:
        return PRESET_MESSAGES["1"][1]

def choose_speed():
    print("\n⚡ Choose typing cadence:")
    print("  [1] Natural Human Pace (0.06s - 0.10s with thinking pauses) [Recommended]")
    print("  [2] Fast & Confident (0.04s per letter)")
    print("  [3] Dreamy & Slow (0.12s per letter)")
    
    speed_choice = input("Enter speed (1-3, default is 1): ").strip()
    if speed_choice == "2":
        return 0.04
    elif speed_choice == "3":
        return 0.12
    else:
        return 0.08  # Default realistic pace

def run_countdown(seconds=5):
    print("\n" + "="*65)
    print("👉 ACTION REQUIRED: YOU HAVE 5 SECONDS!")
    print("   1. Click on Tina's chat box (WhatsApp, Telegram, etc.)")
    print("   2. Make sure your blinking text cursor is inside her input field!")
    print("="*65 + "\n")

    for i in range(seconds, 0, -1):
        heart = "💖" if i % 2 == 0 else "💓"
        print(f"   [{i}] {heart} Click on Tina's chat box now... ({i}s remaining)")
        play_beep(600 + (seconds - i) * 100, 150)
        time.sleep(1)

    print("\n🚀 STARTING MAGIC TYPING! Hands off your keyboard... ✨\n")
    play_beep(1200, 300)
    time.sleep(0.4)

def type_message_with_flair(message, base_speed=0.08):
    total_chars = len(message)
    chars_typed = 0
    
    print("Typing in progress:")
    
    for char in message:
        if char == "\n":
            send_shift_enter()
            # Human-like breath pause at new lines
            time.sleep(0.45)
        else:
            send_unicode_char(char)
            # Add natural human cadence: micro variations
            jitter = random.uniform(-0.02, 0.03)
            delay = max(0.02, base_speed + jitter)
            
            # Longer pause after punctuation like '...' or commas
            if char in [".", ",", "!", "?"]:
                delay += 0.18
            elif char in ["😊", "😏", "❤️", "🍦"]:
                delay += 0.25  # pause as if selecting emoji
                
            time.sleep(delay)
        
        chars_typed += 1
        percent = int((chars_typed / total_chars) * 100)
        bar_len = 30
        filled = int((chars_typed / total_chars) * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(f"\r  [{bar}] {percent}% | Typing message... ")
        sys.stdout.flush()

    print("\n\n🎉 ALL DONE! The message is sitting beautifully in Tina's chat box!")
    
    # Victory fanfare chime
    if HAS_SOUND:
        for f in [523, 659, 784, 1046]:
            play_beep(f, 120)

def main():
    print_banner()
    message = choose_message()
    speed = choose_speed()

    print("\n" + "-"*65)
    print("📜 MESSAGE TO TYPE:")
    print(message)
    print("-"*65)

    input("\n👉 When you are ready, press [ENTER] to begin the 5-second countdown...")

    run_countdown(5)
    type_message_with_flair(message, speed)

    print("\n" + "="*65)
    send_now = input("Would you like to press ENTER to send it now? (y/n, default is n): ").strip().lower()
    if send_now == "y":
        print("Sending in 2 seconds! Click her chat box...")
        time.sleep(2)
        send_enter()
        print("🚀 SENT! Enjoy her reaction! 🥰")
    else:
        print("✨ Left in the chat box! You can review it and click Send whenever you're ready 😉")
    print("="*65 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user. Have a wonderful day!")
