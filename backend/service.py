import schedule
import time
import subprocess
from pynput import keyboard, mouse
from datetime import datetime
import threading

count = 0

class UserActivityMonitor:
    def __init__(self):
        self.active = False
        self._run_listener()

    def _run_listener(self):
        keyboard_listener = keyboard.Listener(on_press=self._set_active)
        mouse_listener = mouse.Listener(on_move=self._set_active, on_click=self._set_active, on_scroll=self._set_active)
        keyboard_listener.start()
        mouse_listener.start()

        # Join the threads to keep the listeners running
        threading.Thread(target=keyboard_listener.join).start()
        threading.Thread(target=mouse_listener.join).start()

    def _set_active(self, *args):
        self.active = True

    def is_user_active(self):
        #time.sleep(timeout)  # wait for 'timeout' seconds to check if there is any user activity
        was_active = self.active
        self.active = False  # reset the activity status
        return was_active

monitor = UserActivityMonitor()

def job():
    global count
    msg = "inactive"
    if monitor.is_user_active():
        msg = "active"

    active_app = subprocess.check_output("""osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true'""", shell=True).decode('utf-8').strip()
    if active_app == "Google Chrome":
        result = subprocess.check_output("""osascript -e 'tell application "Google Chrome" to get title of active tab of window 1'""", shell=True).decode('utf-8').strip()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - I'm {msg}... {count}, current app: {active_app}, current tab: {result}")
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - I'm {msg}... {count}, current app: {active_app}")
    count += 1

schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
