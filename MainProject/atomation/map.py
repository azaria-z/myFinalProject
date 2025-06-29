import yaml



# פונקציה לטעינת קובץ YAML וצרוף פעולות בסיסיות
def load_yaml_with_basic_actions(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data

# טוענים קבצים עם פעולות בסיסיות
device_classes = {
    "light": load_yaml_with_basic_actions(r"D:\temp\Documents\project\Text analysis\home_data\device_data\light.yml"),
    "air conditioner":load_yaml_with_basic_actions(r"D:\temp\Documents\project\Text analysis\home_data\device_data\air conditioner.yml"),
    "coffee machine": load_yaml_with_basic_actions(r"D:\temp\Documents\project\Text analysis\home_data\device_data\coffee_machin.yml")
}










