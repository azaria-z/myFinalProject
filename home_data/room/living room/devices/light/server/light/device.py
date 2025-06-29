num_rooms=5


class Device:

    def __init__(self,name,state=False):
        self.__name=name
        self.__state = state
      
    
    def get_state(self):
        return self.__state
    
    def set_state(self,state):
        if isinstance(state, bool):
            state = "true" if state else "false"
        if state in {"true","false"}:
            self.__state = state
            return f"{self.__name} is on" if state=="true" else f"{self.__name} is off"
    
    def change_state(self):
        self.__state = not self.__state

    def get_name(self):
        return str(self.__name)

    def change_name(self, name):
        self.__name = name
        return True
    def __str__(self):
        return f"Device(name={self.__name}, state={'on' if self.__state else 'off'})"



device= Device(1)  

#מה שיניתי?
#עשיתי פה משתנים פרטיים
#הפכתי את LOCATION ל- NAME