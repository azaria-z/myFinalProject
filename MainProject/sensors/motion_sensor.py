from .sensor_base import SensorBase
import time
from Global_variables import *
# מחלקת חיישן תנועה
class MotionSensor(SensorBase):
    def read_loop(self):
        try:
            with open(self.file_path, "r",encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                while True:
                   with open(self.file_path, "r",encoding="utf-8") as f:
                       for i in range(len(lines)):
                           value = lines[i]
                           if not value:
                               continue
                           time.sleep(2)
        except Exception as e:
           print(f"[ERROR] MotionSensor in {self.room}: {e}")
        time.sleep(2)
         




















































         
# # כאשר יש תנועה - ז"א אומר שיש אדם בבית
#     def enter_person(self):
#             now = datetime.now()
#             hour = now.hour
#             if 6 <= hour < 22:#אם זה בוקר
#                     print(f"[INFO] Motion detected in {self.room}, turning on the light.")
#                   #   task_queue.put((sensor["presence"], task_counter, active_device("light", room, "turn on")))
#                     print("Turn on the light.")
#                     # if light_state["status"]!=True:#תעוד מתי נדלק האור 
#                     #      light_state["start_time"]= datetime.now()
#                     # light_state["status"]=True
#                     #הדלקת המזגן
#                     # task_queue.put((self.room, task_counter, "Turn on the air conditioner."))
#                     print("Turn on the air conditioner.")
#                     # if air_conditioner_state["status"]!=True:#תעוד מתי נדלק המזגן 
#                     #      air_conditioner_state["start_time"]= datetime.now()
#                     # air_conditioner_state["status"]=True
                           
    
