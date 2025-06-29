# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"



from rasa_sdk import FormValidationAction, Action
from typing import Any, Text, Dict, List
from rasa_sdk.events import EventType
from rasa_sdk import Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .map import device_classes
from .automaton import Automation
from .do_request import handle_device_action
# from .init_home import home
import requests
import json

# המבנה נתונים של הבית
with open(r"D:\temp\Documents\project\Text analysis\home_data\home.json", "r", encoding="utf-8") as file:
    home = json.load(file)

# outo = Automation()

# # טוענת את המילים לקובץ האוטומט
# def load_words(file):
#     with open(file, "r", encoding="utf-8") as f:
#         for line in f:
#             word, category = line.strip().split(",")
#             outo.add(word.strip(), category.strip())

# טעינה בעת ייבוא הקובץ (כלומר כאשר השרת עולה)
# file=r"D:\temp\Documents\project\Text analysis\RASAprogect\actions\word.txt"
# load_words(file)



# יש לבדוק לגבי הגדרה של פעולות קיימות ופעולות לא קיימות

# לטפל במקרים שאין בהם את ההגדרה

# האם אפשר בשאלות לשמור את הSETTING למשל לשאול איזה קפה הוא רוצה.

#לטפל בשגיאה שהוא לא מוצא את המכשיר

# טיפול בשאלות ללא מאפיין

# --פונקציה של פעולות פשוטות- כיבוי והדלקה--
class ActiveDeviceAction(Action):
    def name(self) -> str:
        return "active_device_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        device = tracker.get_slot("device")
        room = tracker.get_slot("room")
        action = tracker.get_intent_of_latest_message()# חילוץ הכונה
        device= device.lower()
        room=room.lower()
        print(f"device: {device}, action: {action}, room: {room}")
        handle_device_action(dispatcher,device,room,action)
        return []
        


#-- פונקציה של שינוי הגדרות במכשיר --
    
class ChangeSettingAction(Action):
    def name(self) -> str:
        return "change_setting_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        device = tracker.get_slot("device")
        room = tracker.get_slot("room")
        # setting= tracker.get_slot("setting")
        value=tracker.get_slot("value")
        action =tracker.get_slot("original_intent")# חילוץ הכונה

        print(f"device: {device}, action: {action}, room: {room},value: {value}")
        device= device.lower()
        room=room.lower()
        # setting=setting.lower()
        value=value.lower()
        params = {}
        if action=="add_ingredient" or action=="reduce_ingredient":
            setting= tracker.get_slot("setting")
            setting=setting.lower()
            params["ingredient"] = setting
            params["amount"] = value
        else:
            parts = action.split('_')
            if len(parts) >= 2:
                setting= parts[1]
            params[setting]=value
        handle_device_action(dispatcher,device,room,action,params)
        return [SlotSet("value", None),SlotSet("setting", value)]  # Resetting the value and setting slots after use
        

# --פונקציה שלא חייבת לקבל פרמטרים
class ChangeSettingNotRequiredAction(Action):
    def name(self) -> str:
        return "change_setting_not_required_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        device = tracker.get_slot("device")
        room = tracker.get_slot("room")
        # setting= tracker.get_slot("setting")
        # value=רק אם יש ערך
        action =tracker.get_intent_of_latest_message()# חילוץ הכונה

        print(f"device: {device}, action: {action}, room: {room}")
        device= device.lower()
        room=room.lower()
        action = tracker.get_intent_of_latest_message()# חילוץ הכונה
        value = next(tracker.get_latest_entity_values("value"), None)
        params = {}
        if value is not None:
            value = value.lower()
            parts = action.split('_')
            if len(parts) >= 2:
                setting= parts[1]
            params[setting]=value
        handle_device_action(dispatcher,device,room,action,params)
    
        return []

#--פונקציה של הוספה והורדת רכיבים--

# class IngredientAction(Action):
#     def name(self) -> str:
#         return "ingredient_action"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
#         device = tracker.get_slot("device")
#         # setting= tracker.get_slot("setting")
#         ingredient=tracker.get_slot("ingredient")
#         amount=tracker.get_slot("amount")
#         action = tracker.get_intent_of_latest_message()# חילוץ הכונה
#         room = next(tracker.get_latest_entity_values("room"), None)
#         if room is None:
#            list_device = home["global_devices"][device][0]
#            room = list(list_device.keys())[0]
#         print(f"device: {device}, action: {action}, room: {room}, ingredient: {ingredient}, amount: {amount}")
#         device= device.lower()
#         room=room.lower()
#         ingredient=ingredient.lower()
#         amount=amount
#         params = {}
#         print(f"ingredient: {ingredient}, amount: {amount}")
#         params["ingredient"] = ingredient
#         params["amount"] = amount
        
#         handle_device_action(dispatcher,"coffee machine",room,action,params)
#         return [SlotSet("ingredient", None),SlotSet("amount", None)]  # Resetting the ingredient and amount slots after use


class MakeCoffeeAction(Action):
    def name(self) -> str:
        return "make_coffee_action"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        action = tracker.get_intent_of_latest_message()# חילוץ הכונה
        coffee= tracker.get_slot("coffee")
        print(f"device: coffee machine, action: {action},coffee: {coffee}") 
        coffee=coffee.lower()
        params = {}
        params["coffee"] = coffee
        room = next(tracker.get_latest_entity_values("room"), None)
        if room is None:
           list_device = home["global_devices"]["coffee machine"][0]
           room = list(list_device.keys())[0]
        handle_device_action(dispatcher,"coffee machine",room,action,params)
        return [SlotSet("coffee", None)]  # Resetting the coffee slot after use


class GetIngredientAction(Action):
    def name(self) -> str:
        return "get_ingredient_action"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        action = tracker.get_intent_of_latest_message()# חילוץ הכונה
        ingredient= tracker.get_slot("setting")
        print(f"device: coffee machine, action: {action},ingredient: {ingredient}") 
        ingredient=ingredient.lower()
        params = {}
        params["ingredient"] = ingredient
        room = next(tracker.get_latest_entity_values("room"), None)
        if room is None:
           list_device = home["global_devices"]["coffee machine"][0]
           room = list(list_device.keys())[0]

        handle_device_action(dispatcher,"coffee machine",room,action,params)
        return [SlotSet("setting", None)]  # Resetting the setting slot after use


#--פונקציה של שאלות--

class GetDeviceStatusAction(Action):
    def name(self) -> str:
        return "get_device_status_action"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        device = tracker.get_slot("device")
        room = tracker.get_slot("room")
        action =tracker.get_intent_of_latest_message()# חילוץ הכונה

        # setting=outo.search(setting)
        # if setting ==None:#אין מילה כז באוטומט
        #     dispatcher.utter_message(text=f"Invalid property: {setting}.")
            # return []
        handle_device_action(dispatcher,device,room,action)
        return []


class CoffeeRequestAction(Action):
    def name(self) -> str:
        return "Coffee_request_action"
    

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:

        action =tracker.get_intent_of_latest_message()# חילוץ הכונה
        room = next(tracker.get_latest_entity_values("room"), None)
        if room is None:
           list_devices = home["global_devices"]["coffee machine"][0]
           room = list(list_devices.keys())[0]
        handle_device_action(dispatcher,"coffee machine",room,action)
        return []



#שמירת הכונה הראשונית
class ActionAskClarification(Action):
    def name(self):
        return "action_keep_intent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        original_intent = tracker.latest_message.get("intent", {}).get("name")
        print(f"Original intent saved: {original_intent}")
        return [SlotSet("original_intent", original_intent)]

    


    
#משפט לא מובן
class ActionAskClarification(Action):
    def name(self):
        return "action_ask_clarification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        dispatcher.utter_message(text=(
            "I'm not sure what you want to do."
            "May I please choose: On, Off, or Settings?"
        ))
        return []




# class ValidateYourForm(FormValidationAction):
#     def name(self) -> str:
#         return "validate_change_setting_form"

#     async def required_slots(
#         self,
#         slots_mapped_in_domain: List[str],
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[str, Any],
#     ) -> List[str]:
#         # שמירת הכוונה המקורית אם עדיין לא שמורה
#         if tracker.get_slot("original_intent") is None:
#             original_intent = tracker.latest_message.intent.get("name")
#             return [SlotSet("original_intent", original_intent)] + slots_mapped_in_domain

#         return slots_mapped_in_domain




# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet

# class ActionResetSlots(Action):
#     def name(self):
#         return "action_reset_slots"

#     async def run(self, dispatcher, tracker, domain):
#         return [
#             SlotSet("value", None),
#             SlotSet("device", None),
#             SlotSet("room", None)
#         ]


# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet

# class ActionResetValueSlot(Action):
#     def name(self):
#         return "action_reset_value_slot"

#     def run(self, dispatcher, tracker, domain):
#         return [SlotSet("value", None)]





















































# class ControlDeviceAction(Action):
#     def name(self) -> str:
#         return "active_device_action"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
#         device = tracker.get_slot("device")
#         room = tracker.get_slot("room")
#         action = tracker.latest_message.intent.get("name")# חילוץ הכונה

#         print(f"device: {device}, action: {action}, room: {room}")
#         device= device.lower()
#         room=room.lower()
#         try:
#            if room in home["rooms"]:#האם יש חדר כזה 
#               if device in home["rooms"][room]["devices"]:#האם יש את המכשיר בחדר 
#                 port=home["rooms"][room]["devices"][device]
#                 if port:
#                     if action in device_classes[device]["actions"][action]:# בודקים אם יש כזו פעולה על המכשיר
#                         data=device_classes[device]["actions"][action][device]# כי זה פעולות על המכשיר עצמו
#                         url=data["URL"]
#                         # שם את הפורט של המכשיר
#                         if isinstance(url, str) and "{port}" in url:
#                              url=url.replace("{port}", str(port))
#                              print(f"Final URL: {url}")
#                         else:
#                             dispatcher.utter_message(text=f"ERROR IN URL")
#                             return[]

#                         method=data["method"] 
#                         params = data.get("params",{})
#                         # שליחת הבקשה
#                         response = requests.request(method=method, url=url, json=params)
#                          #  dispatcher.utter_message(text=f"Sent {method} to {url} with params {params}")
#                         dispatcher.utter_message(text=f"Response: {response.status_code}, {response.text}")
#                         if response.text:
#                             try:
#                                 response_data = response.json()
#                                 response_text = response_data.get("message", "")
#                             except ValueError:
#                                 response_text = "The server did not return a valid JSON response."
#                         else:
#                             response_text = "The server did not return a response at all."
                        
    
#                     dispatcher.utter_message(text=str(response_text))
#               else:
#                   dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")
#            else:
#                 dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")
       
#         except KeyError as e:
#           dispatcher.utter_message(text=f"Error type: {type(e).__name__}, message: {e}")
#         return []
        


# #-- פונקציה של שינוי הגדרות במכשיר --
    
# class ControlDeviceAction(Action):
#     def name(self) -> str:
#         return "change_setting_action"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
#         device = tracker.get_slot("device")
#         room = tracker.get_slot("room")
#         setting= tracker.get_slot("setting")
#         value=tracker.get_slot("value")
#         action = tracker.latest_message.intent.get("name")# חילוץ הכונה

#         print(f"device: {device}, action: {action}, room: {room}")
#         device= device.lower()
#         room=room.lower()
#         setting=setting.lower()
#         value=value.lower()
        
#         try:
#            if room in home["rooms"]:#האם יש חדר כזה 
#               if device in home["rooms"][room]["devices"]:#האם יש את המכשיר בחדר 
#                 port=home["rooms"][room]["devices"][device]
#                 if port:
#                     if action in device_classes[device]["actions"][action]:# בודקים אם יש כזו פעולה על המכשיר
#                         data=device_classes[device]["actions"][action][setting]# כי זה פעולות על המכשיר עצמו
#                         url=data["URL"]
#                         # שם את הפורט של המכשיר
#                         if isinstance(url, str) and "{port}" in url:
#                              url=url.replace("{port}", str(port))
#                              print(f"Final URL: {url}")
#                         else:
#                             dispatcher.utter_message(text=f"ERROR IN URL")
#                             return[]

#                         method=data["method"] 
#                         params = data.get("params",{})
#                         params[setting] = value
#                         # שליחת הבקשה
#                         response = requests.request(method=method, url=url, json=params)
#                          #  dispatcher.utter_message(text=f"Sent {method} to {url} with params {params}")
#                         dispatcher.utter_message(text=f"Response: {response.status_code}, {response.text}")
#                         if response.text:
#                             try:
#                                 response_data = response.json()
#                                 response_text = response_data.get("message", "")
#                             except ValueError:
#                                 response_text = "The server did not return a valid JSON response."
#                         else:
#                             response_text = "The server did not return a response at all."
#                             if not setting or not value:
#                                 dispatcher.utter_message(text=f"No required parameters (setting or value) were entered.")
#                                 return []

#                     dispatcher.utter_message(text=str(response_text))
#               else:
#                   dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")
#            else:
#                 dispatcher.utter_message(text=f"Device '{device}' not found in room '{room}'.")
       
#         except KeyError as e:
#           dispatcher.utter_message(text=f"Error type: {type(e).__name__}, message: {e}")
#         return []

































































































































