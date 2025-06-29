
from datetime import datetime
import time

#כאן אני אגדיר את המשתנים הגלובליים

# Global_variables.py
import queue
import threading
from threading import Lock

# תור עם עדיפויות
task_queue = queue.PriorityQueue()

# כדי להבטיח סדר יציב בין משימות עם אותה עדיפות
task_counter = 0
counter_lock = Lock()


sensor_values = {
    "living room": {
        "temperature": 0,
        "humidity": 0,
        "motion": 0,
        "light": 0
    }
   
}
sensor_lock = threading.Lock()

