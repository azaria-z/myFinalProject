from sensors.motion_sensor import MotionSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.presence_sensor import PresenceSensor
from sensors.humidity_sensor import HumiditySensor
# אפשר להוסיף כאן יבוא של חיישנים נוספים לפי הצורך

SENSOR_CLASSES = {
    "motion": MotionSensor,
    "temperature": TemperatureSensor,
    "humidity": HumiditySensor,
    "presence": PresenceSensor,
}

# לכל חיישן יש פעולות שונות שצריך  לבצע עליו
def create_sensor(sensor_name, room, file_path):
    sensor_class = SENSOR_CLASSES.get(sensor_name)
    if sensor_class is None:
        raise ValueError(f"Sensor type '{sensor_name}' is not supported.")
    return sensor_class(sensor_name, room, file_path)

