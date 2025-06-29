
from .sensor_base import SensorBase
import time
from datetime import datetime
from Global_variables import sensor_values, sensor_lock
from device_state import *


class PresenceSensor(SensorBase):
    def read_loop(self):
        try:  
            previous_value = 0
            while True:
                 with open(self.file_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    for i  in range (len(lines)):
                        line=lines[i]
                        current_value = int(line.strip())
                        print(f"[PRESENCE] {self.room}: {current_value}")
                        with sensor_lock:
                            sensor_values[self.room][self.name] = current_value  
                        if current_value == 1 and previous_value == 0:# אדם נכנס לחדר   
                            self.enter_person()
                        if current_value == 0 and previous_value == 1:# אדם יצא מהחדר
                            print(f"[INFO] Person left {self.room}")  
                            # self.leave_person()
                        previous_value = current_value 
                        time.sleep(2)

        except Exception as e:
            print(f"[ERROR] PresenceSensor in {self.room}: {e}")
            time.sleep(2)



    def enter_person(self):
         now = datetime.now()
         hour = now.hour
         if 6 <= hour < 22:#אם זה בוקר
                 print(f"[INFO] Person entered {self.room}")
                 data= get_device_state()# קבלת הקובץ 
                 change = False
                 state = data[self.room]["light"]["state"]
                 if state["value"] == "false":
                        if state["updated_by"] != "user" or has_one_hour_passed(state["last_updated"]):
                            # print("Trying to turn on light...")
                            update_field(data[self.room]["light"]["state"], "true")
                            self.send_task(2, "light", "turn_on")
                            change = True

                 state = data[self.room]["air conditioner"]["state"]
                 if state["value"] == "off":
                    if state["updated_by"] != "user" or has_one_hour_passed(state["last_updated"]):
                        # print("Trying to turn on air conditioner...")
                        update_field(data[self.room]["air conditioner"]["state"], "on")
                        self.send_task(2, "air conditioner", "turn_on")
                 change = True
                 if change:
                     update_device_state(data)












# print(f"[INFO] Motion detected in {self.room}, turning on the light.")
#                  print(handle_device_action("air conditioner", self.room, "turn_on"))
#                  print(handle_device_action("light", self.room, "turn_on"))
#                  print("Turn on the light.")
#                  # task_queue.put((self.room, task_counter, "Turn on the air conditioner."))
#                  print("Turn on the air conditioner.")
#                 #  task_queue.put((2,handle_device_action("air coonditioner", self.room, "turn_on")))
#                                 #   task_queue.put((2,handle_device_action("light", self.room, "turn_on")))

#                  # if air_conditioner_state["status"]!=True:#תעוד מתי נדלק המזגן 
#                  #      air_conditioner_state["start_time"]= datetime.now()
#                  # air_conditioner_state["status"]=True