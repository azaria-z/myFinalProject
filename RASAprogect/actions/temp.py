from typing import List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
import requests

# Placeholder definitions for missing variables
home = {
    "rooms": {
        "living room": {
            "devices": {
                "lamp": 1
            }
        }
    }
}
aaaaa = ["turn_on", "turn_off"]  # Example actions that require parameters
device_classes = {
    "lamp": {
        "actions": {
            "turn_on": {
                "URL": "http://example.com/device/{port}/on",
                "method": "POST",
                "params": {}
            },
            "turn_off": {
                "URL": "http://example.com/device/{port}/off",
                "method": "POST",
                "params": {}
            }
        }
    }
}

class ControlDeviceAction(Action):
    def name(self) -> str:
        return "control_device_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[EventType]:
        device = tracker.get_slot("device")
        action = tracker.get_slot("action")
        room = tracker.get_slot("room")
        print(f"device: {device}, action: {action}, room: {room}")
        device = device.lower()
        action = action.lower()
        room = room.lower()
        try:
            if room in home["rooms"]:
                if device in home["rooms"][room]["devices"]:
                    port = home["rooms"][room]["devices"][device]
                    if port:

                        if action in aaaaa:
                            property = tracker.get_slot("property")
                            value = tracker.get_slot("value")
                            action_obj = device_classes[device]["actions"][action]
                            has_params = True
                        else:
                            action_obj = device_classes[device]["actions"][action]
                            has_params = False
                        url = action_obj["URL"]
                        if isinstance(url, str) and "{port}" in url:
                            url = url.replace("{port}", str(port))
                            print(f"Final URL: {url}")

                        else:
                            dispatcher.utter_message(text=f"ERROR IN URL")
                            return []

                        method = action_obj["method"]
                        params = action_obj.get("params", {})
                        # json.dumps(params)
                        if has_params:  # מתבסס שיש פרמטר אחד
                            params[property] = value
                        response = requests.request(method=method, url=url, json=params)
                        #  dispatcher.utter_message(text=f"Sent {method} to {url} with params {params}")
                        dispatcher.utter_message(text=f"Response: {response.status_code}, {response.text}")
                        if response.text:
                            try:
                                response_data = response.json()
                                response_text = response_data.get("message", "")
                            except ValueError:
                                response_text = "The server did not return a valid JSON response."
                        else:
                            response_text = "The server did not return a response at all."
                        if has_params:
                            if not property or not value:
                                dispatcher.utter_message(text="לא הוזנו פרמטרים נדרשים (property או value).")
                                return []

                        dispatcher.utter_message(text=str(response_text))
                else:
                    dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")
            else:
                dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")

        except KeyError as e:
            dispatcher.utter_message(text=f"Error type: {type(e).__name__}, message: {e}")
        return []
        
