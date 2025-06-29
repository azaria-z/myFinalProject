
from enum import Enum

#יש לבדוק איך זה עובד עם מצבים
class Mode_Air_Conditioner(Enum):
    COOL = "cool"
    HEAT = "heat"
    FAN = "fan"
    DRY = "dry"# מייבש את הלחות בחדר
    SLEEP = "sleep"


class blinds_position(Enum):
    OPEN = "open"
    CLOSE = "close"
    HALF = "half"# חצי פתוח
    SWING= "swing"# נעים
    MEMORY= "memory"# -חוזרים למקום הקודם זכרון
    Auto= "auto"# אוטומטי
    Vertical_Swing = "vertical swing"# נעים אנכי
    Horizontal_Swing = "horizontal swing"# נעים אופקי

class Fun_Speed(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"
    Silent = "silent"# שקט
    Turbo = "turbo"# טורבו
    

    