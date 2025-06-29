from .sensor_base import SensorBase
import time
from datetime import datetime
from Global_variables import *

# מחלקת חיישן לחות
class HumiditySensor(SensorBase):
    def read_loop(self):
         try:
            while True:
               with open(self.file_path,"r",encoding="utf-8") as f:
                   for line in f:
                       value = line.strip()
                       print(f"[HUMIDITY] {self.room}: {value}")
                       time.sleep(2)
         except Exception as e:
            print(f"[ERROR] MotionSensor in {self.room}: {e}")
         
