import yaml

# # פעולות בסיסיות
# basic_actions = {
#     "change": {"name":"set_state","params":[{"type":bool,"value":True}]},
#     "turn off": {"name":"set_state","params":[{"type":bool,"value":False}]},
#     "get status": {"name":"get_state","params":[]},
#     "get name": {"name":"get name","params":[]},
#     "change name": {"name":"change_name","params":[{"type":int,"value":None}]},
# }

# פונקציה לטעינת קובץ YAML וצרוף פעולות בסיסיות
def load_yaml_with_basic_actions(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        # # הוספת פעולות בסיסיות לכל קובץ
        # if "actions" in data:
        #     data["actions"].update(basic_actions)
        return data

# טוענים קבצים עם פעולות בסיסיות
device_classes = {
    "light": load_yaml_with_basic_actions(r"D:\temp\Documents\project\Text analysis\home_data\device_data\light.yml"),
    "air conditioner":load_yaml_with_basic_actions(r"D:\temp\Documents\project\Text analysis\home_data\device_data\air conditioner.yml"),
    "coffee machine": load_yaml_with_basic_actions(r"D:\temp\Documents\project\Text analysis\home_data\device_data\coffee_machin.yml")
}

# דוגמה לשימוש
# print(device_classes["light"]["actions"])









# basic_actions:
#   change:
#     name: set_state
#     params:
#       - type: bool
#         value: true
#   turn off:
#     name: set_state
#     params:
#       - type: bool
#         value: false
#   get status:
#     name: get_state
#     params: []
#   get name:
#     name: get name
#     params: []
#   change name:
#     name: change_name
#     params:
#       - type: int
#         value: null
