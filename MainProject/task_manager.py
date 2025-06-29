from Global_variables import task_queue
import threading

def task_manager():
    while True:
        priority, task_callable = task_queue.get()
        print(f"\n Executing task with priority {priority}")
        try:
            task_callable()  # מבצע את הפעולה
        except Exception as e:
            print(f" Error while executing task: {e}")
        task_queue.task_done()


def start_task_manager():
    thread = threading.Thread(target=task_manager, daemon=True)
    thread.start()
