
import json
from .device import Device
from .mode_Air_Conditioning import Mode_Air_Conditioner,blinds_position,Fun_Speed

class Air_Conditioner(Device):
    
     def __init__(self,name="air conditioner", state=False, temperature=24, mode="cool", fan_speed="medium"):
         super().__init__(name,state)
         self.__statuse_mode=self.load_status_mode()
         self.__temperature = temperature
         self.__mode = mode
         self.__fan_speed = fan_speed
         self.blinds_position=blinds_position.OPEN.name#מיקום התריס
         self.display="off"#תצוגה של המזגן
         self.louver_angle = 50#זווית התריס

     def load_status_mode(self):
        with open(r"D:\temp\Documents\project\Text analysis\python_project\devices\air_condition\mode.json", "r") as file:
            data = json.load(file)
            return data
  
     #שינוי מצב מזגן   
     def change_mode(self, mode_name):
         mode_name = mode_name.upper()
         if mode_name in Mode_Air_Conditioner.__members__:
            mode_settings = self.__statuse_mode[mode_name]
            if mode_settings:
                self.__mode=mode_settings["mode"]
                self.__temperature=mode_settings["temperature"]
                self.__fan_speed=mode_settings["fan_speed"]
                self.display=mode_settings["display"]
                self.blinds_position=mode_settings["blinds_position"]
                self.louver_angle=mode_settings["louver_angle"]

                return f"mode changed to {mode_name}."
         else:
             return "Invalid mode."
    
         
     #שינוי טמפרטורה 
     # כולל הקטנה והגדלה   
     def change_temperature(self, temperature=None, increase=None):
        if temperature is None:
            temperature=2
        temperature=int(temperature)
        if increase is not None:
            if not increase:
                temperature= -temperature
            temperature=self.__temperature +temperature
        if 16 <= temperature <= 30:
            self.__temperature = temperature
            self.save_state("temperature", temperature)
            return f"temperature changed to {temperature}."
        return "Temperature must be between 16 and 30."


    #כל שינוי נשמר ב-JSON כדי שבפעם הבאה יוכלו לדעת את המצב הנוכחי
        #שינוי המהירות של המאורר
     def change_fan_speed(self, fan_speed):
        if fan_speed in Fun_Speed: 
            self.fan_speed = fan_speed
            self.save_state("fan_speed", fan_speed)
            return f"fan speed changed to {fan_speed}."
        else:
            return "Invalid fan speed."
        
         
     #שינוי מיקום התריס   
     def change_blinds_position(self, new_blinds_position):
        if new_blinds_position in blinds_position:
            self.blinds_position = new_blinds_position
            self.save_state("blinds position", new_blinds_position)
            return f"blinds position changed to {new_blinds_position}."
        else:
            return "Invalid blinds position."

    #שינוי מצב תצוגה 
     def set_display(self, display_state):
         if isinstance(display_state, bool):
            display_state = "on" if display_state else "off"
         if display_state not in ["on", "off"]:
             print (display_state)
             return "Invalid display state. Use 'on' or 'off'."
         self.display = display_state
         self.save_state("display", display_state)
         return f"display is {display_state}."
     
     #שינוי זווית התריס
     def change_louver_angle(self, louver_angle):
        if 0 <= louver_angle <= 90:
            self.louver_angle = louver_angle
            self.save_state("louver_angle", louver_angle)
            return f"louver angle changed to {louver_angle}."
        
        else:
            return "louver angle must be between 0 and 90."
        

     def save_state(self,name,value):  
       self. __statuse_mode[self.__mode.upper()][name] = value

     def get_state_mode(self):
         return {
             "mode": self.__mode,
             "temperature": self.__temperature,
             "fan_speed": self.__fan_speed,
             "display": self.display,
             "blinds_position": self.blinds_position,
             "louver_angle": self.louver_angle,
             "state": "on" if self.get_state() else "off",
             "name": self.get_name()
         }
     
     def get_action_status(self, action_name=None):
        status = self.get_state_mode()  # שליפת המצב הנוכחי של המזגן
        #מפה בין שם הפעולה לשם 
        action_to_status_key = {
            "temperature": "temperature",
            "mode": "mode",
            "fan_speed": "fan_speed",
            "blinds": "blinds_position",
            "display": "display",
            "louverangle": "louver_angle", }
        if action_name is None:
            return status  # לא נשלחה פעולה — מחזיר את כל המצב
        key = action_to_status_key.get(action_name.lower())
        if key is not None:
            return {key: status.get(key)}  # מחזיר רק את הפריט המבוקש
        return f"This property is not defined: {action_name}"  # אם הפעולה לא מוכרת — מחזיר את כל המצב



     



     
















































































































        #להוסיף עוד פונקציות ולכתוב את הקוד בצורה יותר מסודרת
        # לבדוק שהקוד עובד




           # #הקטנת מהירות המאורר
    #  def decrease_fan_speed(self):
    #      if Fun_Speed.index(self.__fan_speed) > 0:
    #          self.__fan_speed = Fun_Speed[Fun_Speed.index(self.__fan_speed) - 1]
    #          self.save_state("fan_speed", self.__fan_speed)
    #          return f"fan speed decreased to {self.__fan_speed}."
    #      else:
    #             return "Fan speed cannot be less than low."

    #   #הגדלת מהירות המאורר   
    #  def increase_fan_speed(self):
    #         if Fun_Speed.index(self.__fan_speed) < len(Fun_Speed) - 1:
    #             self.__fan_speed = Fun_Speed[Fun_Speed(self.__fan_speed) + 1]
    #             self.save_state("fan_speed", self.__fan_speed)
    #             return f"fan speed increased to {self.__fan_speed}."
    #         else:
    #             return "Fan speed cannot be greater than turbo."
         