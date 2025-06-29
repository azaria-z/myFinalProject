from .device import Device
from .amount import coculate_amount
import json




class Coffee_Machine(Device):

    def __init__(self, name="Coffee Machine",coffee=0, water=0, sugar=0, milk=0, chocolate=0, water_level=0):
        super().__init__(name)
        self.__ingredients = {'coffee': {'amount':coffee,'copacity':100}, 'water': {'amount':water,'copacity':300}, 'sugar': {'amount':sugar,'copacity':100}, 'milk': {'amount':milk,'copacity':300}, 'chocolate': {'amount':chocolate,'copacity':100}}
       
        self.__coffee_types = self.load_type()
        # self.__water_level = water_level  # רמת המים במכונה    
    def load_type(self):
        with open(R"D:\temp\Documents\project\Text analysis\home_data\room\living room\devices\coffee\coffee_machine\coffee_properties.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
        
   #הוספת מרכיב קפה
    def add_ingredient(self, name, amount):
        if name not in self.__ingredients:
            return f"Ingredient '{name}' not found."
        current = self.__ingredients[name]["amount"]
        capacity = self.__ingredients[name]["copacity"]
        if current + amount <= capacity:
            self.__ingredients[name]["amount"] += amount
            return f"Added {amount} units of {name}. New level: {self.__ingredients[name]["amount"]}"
        return f"The machine can contain up to {capacity} units of {name}."
    
    #הורדת כמות של מרכיב קפה
    def reduce_ingredients(self,ingredient,amount):
        if self.__ingredients[ingredient]['amount'] - amount >= 0:
            self.__ingredients[ingredient]['amount'] -= amount
            return (f"Removed {amount} units of {ingredient}. New level: {self.__ingredients[ingredient]["amount"]}")
        return (f"Sorry, not enough {ingredient}")
  
    #קבלת כמות של מרכיב במכונה
    def get_ingredient(self, name):
        ingredient = self.__ingredients.get(name)
        if ingredient:
            ingredient=ingredient['amount']
            return ingredient
        return f"Ingredient '{name}' not found."

    # מצב כל המרכיבים במכונה
    def get_ingredients_status(self):
        lines = ["Current ingredients status:"]
        for name, data in self.__ingredients.items():
             lines.append(f"- {name.capitalize()}: {data['amount']} / {data['copacity']} units")
        return "\n".join(lines)

# אני מחזירה את הכל בפורמט JSON
    def get_ingredients_json(self):
        return self.__ingredients


    #קבלת רמת המים

   
    def make_coffee(self, coffee_type='regular'):
        if self.get_state():
            coffee = self.__coffee_types.get(coffee_type)  # מקבל את סוג הקפה
            if coffee:  # יש קפה כזה 
                # בדיקה אם יש מספיק מצרכים
                for ingredient_info in coffee['ingredients']:  # מעבר על כל המצרכים
                    ingredient = ingredient_info['ingredient']  # המצרך  
                    required_amount = ingredient_info['amount']  # כמות המצרך
                    if not self.is_enough_ingredient(ingredient, required_amount):
                        return (f"Sorry, not enough {ingredient}."+f"\n Required: {required_amount}. Available: {self.__ingredients[ingredient]['amount']}")
                    else:
                        self.reduce_ingredients(ingredient,coculate_amount(required_amount))
                # המתנה לזמן הקפה אולי אשלח הודעה למערכת
                # time.sleep(coffee['brewing_time'])  # זמן הכנה
                return(f"{coffee_type.capitalize()} coffee is ready!")
            else:
                return(f"Sorry, {coffee_type} is not a valid coffee type.")
        return(f"turn on the coffee please")
    
    # הפונקציה הזו בודקת אם יש מספיק חומר במלאי
    def is_enough_ingredient(self, ingredient, required_amount): 
        try: 
            if ingredient not in self.__ingredients:
                return False
            amount = coculate_amount(required_amount)  # הכמות שהשארה לי מהמוצר
            # הפוך את המידות לכל מיליליטר/כפות או כוסות/גרם בהתאם לכמות
            ingredients_value = self.__ingredients[ingredient]["amount"]  # הכמות שהשארה לי מהמוצר 
            return ingredients_value >= amount
        except Exception as e:
            print("your exaption is: " + str(e))
    
    # קבל כל סוגי הקפה
    def get_coffee_types(self):
      return list(self.__coffee_types.keys())

    # קבלת מצרכים של קפה
    def get_coffee_ingredient(self,coffee_type):
        ingredients = self.__coffee_types[coffee_type]["ingredients"]
        return "\n".join(f"{item['ingredient']}:{item['amount']}" for item in ingredients)

# הוספת קפה
# שינוי קפה
# הוספת מצרכים







































    # def get_water_level(self):
    #     return self.__water_level
    
    # # amount חיובי – מתבצעת הוספה.
    # #amount שלילי – מתבצעת הפחתה
    # def update_water_level(self, amount,increase=True):
    #     if not increase:
    #         amount=-amount
    #     new_level = self.__water_level + amount
    #     if 0 <= new_level <= 100:
    #         self.__water_level = new_level
    #         action = "Added" if amount > 0 else "Removed"
    #         return f"{action} {abs(amount)} units of water. New level: {self.__water_level}"   
    #     return "Invalid operation: water level must stay between 0 and 100 units."











 #כתיבה לקובץ JSON

#פונקציה של שמירת סוג קפה חדש
#במידה ואספיק ארשום אותה

#  def add_new_coffee(self, file_path, coffee_name, strength, temperature, has_milk_froth, brewing_time, water_level, ingredients, comment):
#             # בדיקה אם הקפה כבר קיים
#         if coffee_name in self.__coffee_types:
#             return("the coffee already exists")
#             # הוספת קפה חדש
#         self.__coffee_types [coffee_name] = {
#                 "strength": strength,
#                 "temperature": temperature,
#                 "has_milk_froth": has_milk_froth,
#                 "brewing_time": brewing_time,
#                 "water_level": water_level,
#                 "ingredients": ingredients,
#                 "comment": comment
#             }
#         self.save_coffee_types(file_path, self.__coffee_types)
#         return("the coffee has been added")

    #שמירת סוג קפה חדש
    # def save_coffee_types(self, coffee_types_file, coffee_data,):
    #      try:
    #          with open(coffee_types_file, "a", encoding="utf-8") as file:
    #             json.dump(coffee_data, file, indent=4)
    #             print("success")
    #      except Exception as e:
    #         print("fail")

