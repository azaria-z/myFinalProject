import requests
import json
from atomation.map import device_classes
with open(r"D:\temp\Documents\project\Text analysis\home_data\home.json", "r", encoding="utf-8") as file:
    home = json.load(file)

# פונקציה שעושה את שליחת בקשה למכשיר

# לשים לב לשלוח את הפרמטרים הנוספים לבד
def handle_device_action(device,room,action,params_form={}):
    
    if room not in home["rooms"]:
        print(f"Room '{room}' not found.")
        return

    if device not in home["rooms"][room]["devices"]:
        print(f"Device '{device}' not found in room '{room}'.")
        return

    port = home["rooms"][room]["devices"][device]
    if not port:
        print(f"Port for device '{device}' not found.")
        return

    try:
        if action not in device_classes[device]["actions"]:
            print(f"Action '{action}' not supported for device '{device}'.")
            return

        else:
            data = device_classes[device]["actions"][action]
        url = data["URL"]
        if isinstance(url, str) and "{port}" in url:
            url = url.replace("{port}", str(port))
            # print(f"URL:'{url}'")
        else:
            print("ERROR IN URL")
            return
        params = data.get("params", {})
        method = data["method"]# סוג הבקשה 
        if method == "GET":# בבקשת GET אין גוף לבקשה
            if params_form:#אם יש ערך
                for key, value in params_form.items():
                    if key in params:
                        if isinstance(url, str) and "{key}" in url:
                            url = url.replace("{key}", str(value))
                            print(f"URL:'{url}'")
        else:# שמים את הפרמטרים בגוף הבקשה
            if params_form:#אם יש ערך
                for key, value in params_form.items():
                    if key in params.keys():
                        params[key] = value
                        # print(f"key:{key} value:{value}")
                    else:
                        print(f"Parameter '{key}' not found in device action parameters.")
                        return
                       
        try:
            response = requests.request(method=method, url=url, json=params)
        except requests.exceptions.RequestException as e:
            print(f"I can't find the device: {e}")
            return

        if response:
            # print(f"Response: {response.status_code}, {response.text}")
            try:
                response_data = response.json()
                if isinstance(response_data, dict):
                    response_text = response_data.get("message", "")
                else:
                    response_text = str(response_data)  # זה יכול להיות list או str
            except ValueError:
                response_text = f"The server did not return a valid JSON response: {response.text}"

            print(f"[Automation] {response_text}")

        else:
            print(f"{response}")
            print("no response")


    except KeyError as e:
        print(f"Error type: {type(e).__name__}, message: {e}")





# import json
# from filelock import FileLock

# def update_device(room, device, new_value, changed_by):
#     with FileLock("home_state.json.lock"):
#         with open("home_state.json", "r", encoding="utf-8") as f:
#             data = json.load(f)
        
#         # נניח שיש לך מבנה כזה
#         data["rooms"][room]["devices"][device] = new_value
#         data["rooms"][room]["devices_meta"] = {
#             "last_changed_by": changed_by,
#             "timestamp": time.time()
#         }

#         with open("home_state.json", "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2)

#     print(f"{device} in {room} updated by {changed_by} to {new_value}")
