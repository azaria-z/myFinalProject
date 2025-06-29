from .lightColor import LightColor
from .device import Device

#הגדרת מחלקת אור
class Light(Device):
    #הגדרת תכונות של האור
    def __init__(self, name="light", color=LightColor.WHITE, brightness=50):
        super().__init__(name)
        self.__color = color       
        self.__brightness = brightness

    #שינוי צבע אור   
    def set_color(self, color_name):
        try:
            if  color_name.upper() in LightColor.__members__:
                self.__color = LightColor[color_name.upper()].name
                return f"light color set to {color_name}."
            else:
                return f"Invalid color."
        except Exception as e:
            return f"Error: {e}"
        
    def get_color(self):
        return str(self.__color)

    #שינוי עוצמת אור
    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.__brightness = brightness
            return f"light brightness set to {brightness}."
        else:
            return "Brightness must be between 0 and 100"
        
    #הקטנת עוצמת אור   
    def decrease_brightness(self, amount=10):
        return self.set_brightness(self.__brightness - amount)
        
    #הגדלת עוצמת אור   
    def increase_brightness(self, amount=10):
        return self.set_brightness(self.__brightness + amount)
       
    def get_brightness(self):
        return str(self.__brightness)
    
   














#    #הדלקת אור
#     def turn_on(self):
#         if super().status:
#             return f"the light is already on."
#         super().change_status()
#         return f"light is on."

#     #כיבוי אור
#     def turn_off(self):
#         if not super().status:
#             return f"the light is already off."
#         super().change_status()
#         return f"light is off."