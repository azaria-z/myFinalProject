import threading
from Global_variables import task_queue, counter_lock, task_counter  # ייבוא התור הגלובלי
from action_device import handle_device_action
# from task_manager import task_manager

# מחלקת הבסיס של חיישן
class SensorBase:
    def __init__(self, name, room, file_path):
        self.name = name
        self.room = room
        self.file_path = file_path

    def run(self):
        thread = threading.Thread(target=self.read_loop, daemon=True)
        thread.start()

    def read_loop(self):
        raise NotImplementedError("Must be implemented in subclass")

    def send_task(self, priority, device, action, params={}):
        global task_counter
        with counter_lock:
            task_counter += 1
            final_priority = (priority, task_counter)
        task_queue.put((final_priority, lambda: handle_device_action(device, self.room, action, params)))
        print("sent the task to the queue")
