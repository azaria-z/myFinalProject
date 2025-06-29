


from typing import Optional, Dict
import requests
import json
# Import CollectingDispatcher from rasa_sdk if using Rasa
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .map import device_classes
from .device_state import *
with open(r"D:\temp\Documents\project\Text analysis\home_data\home.json", "r", encoding="utf-8") as file:
    home = json.load(file)

# פונקציה שעושה את שליחת בקשה למכשיר

def handle_device_action(
    dispatcher: CollectingDispatcher,
    device: str,
    room: str,
    action: str,
    # setting= None,
    params_form={}
) -> None:
    
    if room not in home["rooms"]:
        dispatcher.utter_message(text=f"Room '{room}' not found.")
        return

    if device not in home["rooms"][room]["devices"]:
        dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")
        return

    port = home["rooms"][room]["devices"][device]
    if not port:
        dispatcher.utter_message(text=f"Port for device '{device}' not found.")
        return

    try:
        if action not in device_classes[device]["actions"]:
            dispatcher.utter_message(text=f"Action '{action}' not supported for device '{device}'.")
            return
# מתחיל לבצע את הבקשה
        else:
            data = device_classes[device]["actions"][action]
        url = data["URL"]
        if isinstance(url, str) and "{port}" in url:
            url = url.replace("{port}", str(port))
            print(f"URL:'{url}'")
        else:
            dispatcher.utter_message(text="ERROR IN URL")
            return
        params = data.get("params", {})
        method = data["method"]# סוג הבקשה 
        if method == "GET":# בבקשת GET אין גוף לבקשה
            if params_form:#אם יש ערך
                for key, value in params_form.items():
                    print(f"key:{key} value:{value}")
                    if isinstance(url, str) and  f"{{{key}}}" in url:
                        url = url.replace( f"{{{key}}}", str(value))
                        print(f"URL:'{url}'")
        else:# שמים את הפרמטרים בגוף הבקשה
            if params_form:#אם יש ערך
                for key, value in params_form.items():
                    if key in params.keys():
                        params[key] = value
                        print(f"key:{key} value:{value}")
                    else:
                        print(f"Parameter '{key}' not found in device action parameters.")
                        return
                       
        try:
            response = requests.request(method=method, url=url, json=params)
        except requests.exceptions.RequestException as e:
                dispatcher.utter_message(text=f"I can't find the device")
                return

        if response:
            print(f"Response: {response.status_code}, {response.text}")
            try:
                response_data = response.json()
                if isinstance(response_data, dict):
                    response_text = response_data.get("message", "")
                    if response_text== "":
                        response_text = response_data.get("error", "")
                else:
                    response_text = str(response_data)  # זה יכול להיות list או str
            # מעדכן את הדף
            
                # setting=params[0].key
                # print(f"setting:{setting}")
                # update_field(device_state[room][device][setting], response_text)
            except ValueError:
                response_text = f"The server did not return a valid JSON response: {response.text}"

            dispatcher.utter_message(text=str(response_text))
        else:
            print(f"{response}")
            dispatcher.utter_message(text=f"no response")


    except KeyError as e:
        dispatcher.utter_message(text=f"Error type: {type(e).__name__}, message: {e}")
