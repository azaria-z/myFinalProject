import filelock
import json

with open(r"D:\temp\Documents\project\Text analysis\home_data\device_state.json", "r", encoding="utf-8") as f:
    device_state = json.load(f)


from filelock import FileLock, Timeout
import json
import time

file_path = r"D:\temp\Documents\project\Text analysis\home_data\device_state.json"
lock_path = file_path + ".lock"
LOCK_TIMEOUT = 5
RETRY_DELAY = 2

def wait_for_lock(lock):
    while True:
        try:
            lock.acquire(timeout=LOCK_TIMEOUT)
            return
        except Timeout:
            print(f"Lock is busy, waiting {RETRY_DELAY} seconds and trying again...")
            time.sleep(RETRY_DELAY)

#קריאה של הנתונים
#רק מביא את הקובץ הנוכחי
def get_device_state():
    lock = FileLock(lock_path)
    wait_for_lock(lock)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    finally:
        lock.release()

#עדכון של מצב המכשיר
def update_device_state(data):
    lock = FileLock(lock_path)
    wait_for_lock(lock)
    try:    
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        # print("Update successful.")
    finally:
        lock.release()

# פונקציה שבודקת אם עבר שעה מאז שהמשתמש שינה
from datetime import datetime, timedelta

def has_one_hour_passed(last_changed_time):
    time_str = last_changed_time
    start_time = datetime.fromisoformat(time_str)  # הופך מחרוזת לאובייקט datetime

    now = datetime.now()  # הזמן הנוכחי

    # בודקים אם עבר יותר משעה מ־start_time
    if now - start_time > timedelta(hours=1):
        return True
    else:
        return False
    
def update_field(section: dict, value, changed_by="user"):
    section.update({
        "value": value,
        "last_updated": datetime.now().isoformat(),
        "updated_by": changed_by
    })