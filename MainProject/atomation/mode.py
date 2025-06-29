#פה אני מגדירה את כל האוטומציות
import json
from action_device import  handle_device_action
import schedule
from .camera_recording import *
from .take_a_picture  import capture_image
from .face_recognization import recognize_man
from Global_variables import sensor_values, sensor_lock
import threading
# import ctypes
import keyboard


with open(r"D:\temp\Documents\project\Text analysis\home_data\home.json", "r", encoding="utf-8") as file:
    home = json.load(file)


def get_sensor_value(room, sensor_name):
    with sensor_lock:
        room_sensors = sensor_values.get(room, {})
        return room_sensors.get(sensor_name)


# האוטומציה של הבית
#יש דברים שאני עושה בסימולציה רק בשביל האוטומציה
#אוטומציה לילה
def night():
    for room_name, room_data in home["rooms"].items():
        print(f"Night mode in {room_name}")
        #מכבים את האורות בחדר
        port_light = room_data.get("devices", {}).get("light")
        if port_light:
                val = get_sensor_value(room_name, "presence")  # דוגמה
                if not val:  # אין איש בחדר
                    handle_device_action("light", room_name, "turn_off")
# הורדת תריסים
        print("Blinds down")
        #דלקת מצלמות האבטחה
        if room_data["camera"]:  # יש מצלמה
            # פונקצי של הסרטה במצלמה
            start_recording()
        #מכבה את כל המכשירים שלא נצרכים בבית
        for device in room_data["devices"]:
            device_name = room_data["devices"][device]
            if device_name != "light":
                print(f"turn off {device}")
    for hallway_name, hallway_data in home["hallway"].items():
        port_light = hallway_data["devices"].get("light")
        if port_light:
             val = get_sensor_value(hallway_name, "presence")  # דוגמה
             if not val:#אין איש בחדר 
                handle_device_action("light",hallway_name,"turn_on")
             if hallway_data["camera"]: #יש מצלמה
                # start_recording()# יש לי רק מצלמה אחת
                pass



#זיהוי החוזר הביתה
def recognize_visitor():
    path=capture_image()
    #הפעלת קוד של זיהוי פנים
    name=recognize_man(path)
    if name != "guest":
      #יש לודיע מי נכנס לבית
      message= (name)
    else:
      message= (name)
    print(message)



















# if __name__ == "__main__":
#     recognize_visitor()



# while True:

#   schedule.every().day.at("22:47").do(night)
