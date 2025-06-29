import json
from sensor_factory import create_sensor
import threading
import time
from assisment.assissment import Assistant
from task_manager import start_task_manager
from atomation.mode import *
from atomation.camera_recording import stop_recording
import os
import signal
import sys
import shutil
import schedule

HOME_DATA= r"D:\temp\Documents\project\Text analysis\home_data\home.json"
ACTIVE_FILE = r"D:\temp\Documents\project\Text analysis\home_data\device_state.json"
BACKUP_FILE = r"D:\temp\Documents\project\Text analysis\home_data\device_state_backup.json"

#גיבוי הקובץ שיחזו למצב המקורי 
def backup_file():
    if not os.path.exists(BACKUP_FILE):
        shutil.copy(ACTIVE_FILE, BACKUP_FILE)

# שחזור הקובץ למצב המקורי
def restore_file():
    shutil.copy(BACKUP_FILE, ACTIVE_FILE)
    print("\n JSON file restored to its initial state.")
    print("close the camera recording")
    stop_recording()  # מפסיק את ההקלטה אם היא פעילה
    sys.exit(0)

#  סגירת התוכנית ע"י CTRL C
def signal_handler(sig, frame):
    restore_file()


def start_all_sensors(allSensors):
    for room, room_data in allSensors["rooms"].items():
        for sensor_name, path in room_data["sensor"].items():
            sensor = create_sensor(sensor_name, room, path)
            sensor.run()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
schedule.every().day.at("01:11").do(night)


# def on_r_press():
    
#     threading.Thread(target=recognize_visitor).start()
def do_action():
    print("הופעלה פעולה בעקבות לחיצה על R")

def keyboard_listener():
    keyboard.add_hotkey('r', lambda: threading.Thread(target=recognize_visitor, daemon=True).start())
    keyboard.wait()



def main():


    # טיפול ב־CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

     # מריצים את העוזרת בתהליך נפרד
    # assistant_process = Process(target=Assistant)
    # assistant_process.daemon = True  # אפשר להוריד את זה אם רוצים שליטה שונה
    # assistant_process.start()
    threading.Thread(target=Assistant, daemon=True).start()


    backup_file()
    with open(HOME_DATA, "r", encoding="utf-8") as file:
        allSensors = json.load(file)
        start_all_sensors(allSensors)

    start_task_manager()
    # להתחיל את התזמון בתהליכון נפרד
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    threading.Thread(target=keyboard_listener, daemon=True).start()




    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()































