import time
import argparse
import subprocess
import shutil
import sys
from datetime import datetime

def notify(title: str, text: str):
    try:
        if sys.platform == "darwin":
            # macOS notification
            safe_title = title.replace('"', '\\"')
            safe_text = text.replace('"', '\\"')
            subprocess.run(['osascript', '-e', f'display notification "{safe_text}" with title "{safe_title}"'],
                           check=False)
        elif sys.platform.startswith("linux"):
            # Linux notify-send if available
            if shutil.which("notify-send"):
                subprocess.run(['notify-send', title, text], check=False)
            else:
                print(f"[{title}] {text}")
        elif sys.platform.startswith("win"):
            # simple Windows message box (no dependency)
            try:
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, text, title, 0)
            except Exception:
                print(f"[{title}] {text}")
        else:
            print(f"[{title}] {text}")
    except Exception:
        print(f"[{title}] {text}")

def main():
    p = argparse.ArgumentParser(description="Simple command-line hydration reminder.")
    p.add_argument("-i", "--interval", type=int, default=3600,#time or inerval in seconds can be edited
                   help="Interval between reminders in seconds (default 3600).")
    p.add_argument("-m", "--message", default="Time to drink water!",
                   help="Reminder message to display.")
    args = p.parse_args()

    interval = max(1, args.interval)
    print(f"Reminder running every {interval} second(s). Press Ctrl-C to stop.")
    try:
        while True:
            time.sleep(interval)
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{ts}] {args.message}")
            notify("Hydration Reminder", args.message)
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    main()
