
from .sensor_base import SensorBase
import time
from datetime import datetime
from Global_variables import sensor_values, sensor_lock
from device_state import *

class TemperatureSensor(SensorBase):
    def read_loop(self):
       try:
                
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                while True:
                    for line in lines:
                        value = line.strip()
                        # print(f"[TEMPERATURE] {self.room}: {value}")
                        value = float(value)
                        with sensor_lock:
                            sensor_values[self.room][self.name] = value
                        if value < 22:
                            data=get_device_state()
                            change= False
                            state = data[self.room]["air conditioner"]["state"]

                            if state["value"]== "off":
                                if state["updated_by"] != "user" or has_one_hour_passed(state["last_updated"]):
                                    update_field(data[self.room]["air conditioner"]["state"], "on")
                                    self.send_task(2, "air conditioner", "turn_on")
                                    change = True

                            if data[self.room]["air conditioner"]["mode"]["value"] != "cool":
                                if state["updated_by"] != "user" or has_one_hour_passed(state["last_updated"]):
                                    update_field(data[self.room]["air conditioner"]["mode"], "cool")
                                    self.send_task(2, "air conditioner", "change_mode",{"mode": "cool"})
                                    change = True

                            temp = data[self.room]["air conditioner"]["temperature"]["value"]
                            temp = float(temp)
                            if not (25 <= temp <= 30):
                                update_field(data[self.room]["air conditioner"]["temperature"], "26")
                                change = True
                                self.send_task(2, "air conditioner", "change_temperature", {"temperature": "26"})
                            if change:
                                update_device_state(data)
                            print(f"[TEMPERATURE] {self.room}: {value}")
                        time.sleep(1)
    
       except Exception as e:
           print(f"[ERROR] TemperatureSensor in {self.room}: {e}")
           time.sleep(2)





