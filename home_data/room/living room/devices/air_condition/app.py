from flask import Flask, request, jsonify,render_template
from  AC.air_conditioner import Air_Conditioner  # תחליף בייבוא הרלוונטי שלך

app = Flask(__name__)

#מבחינת היגיון יש עוד כמה דברים לשנות אני בע"זה צריכה חעבור על זה שוב


# יצירת מופע של המזגן
ac = Air_Conditioner()

@app.route('/ac/state', methods=["POST"])
def change_ac_state():
    data = request.json
    state = data.get("state")
    if state is not None:
        result = ac.set_state(state)
        return jsonify({"message": result})
    return jsonify({"message": "Invalid state value"}), 400

# שינוי מצב
@app.route('/ac/mode', methods=['POST'])
def change_mode():
    data = request.json
    mode = data.get('mode')
    if not mode:
        return jsonify({"error": "Missing 'mode' parameter"}), 400
    result = ac.change_mode(mode)
    return jsonify({"message": result})

#העלאת טמפרטורה
@app.route('/ac/increase_temperature', methods=['POST'])
def increase_temperature():
    data = request.json
    temperature = data.get('temperature')
    result = ac.change_temperature(temperature, True)
    return jsonify({"message": result})

#הורדת טמפרטורה
@app.route('/ac/decrease_temperature', methods=['POST'])
def decrease_temperature():
    data = request.json
    temperature = data.get('temperature')
    result = ac.change_temperature(temperature,False)
    return jsonify({"message": result})

#שינוי טמפרטורה
@app.route('/ac/temperature', methods=['POST'])
def change_temperature():
    data = request.json
    temperature = data.get('temperature')
    result = ac.change_temperature(int(temperature))
    return jsonify({"message": result})


@app.route('/ac/fan_speed', methods=['POST'])
def change_fan_speed():
    data = request.json
    fan_speed = data.get('fanSpeed')
    if not fan_speed:
        return jsonify({"error": "Missing 'fan_speed' parameter"}), 400
    result = ac.change_fan_speed(fan_speed)
    return jsonify({"message": result})

@app.route('/ac/blinds', methods=['POST'])
def change_blinds():
    data = request.json
    blinds = data.get('blinds')
    if not blinds:
        return jsonify({"error": "Missing 'blinds' parameter"}), 400
    result = ac.change_blinds_position(blinds)
    return jsonify({"message": result})

@app.route('/ac/display', methods=['POST'])
def turn_on_display():
    data = request.json
    state = data.get('state')
    result = ac.set_display(state)
    return jsonify({"message": result})

@app.route('/ac/louver_angle', methods=['POST'])
def change_louver_angle():
    data = request.json
    angle = data.get('louverAngle')
    if angle is None:
        return jsonify({"error": "Missing 'louver angle' parameter"}), 400
    try:
        angle = int(angle)
    except ValueError:
        return jsonify({"error": "'louver angle' must be an integer"}), 400
    result = ac.change_louver_angle(angle)
    return jsonify({"message": result})


#המצב של המזגן
@app.route('/ac/all_status_mode', methods=['GET'])
def all_status_mode():
    result = ac.get_state_mode()
    return jsonify(result)

@app.route('/ac/status/<setting>', methods=['GET'])
def get_status(setting):
    result=ac.get_action_status(setting)
    if result is not None:
        result=  list(result.values())[0]
        print(result)
    return jsonify({"message": result})



@app.route("/ac/name", methods=["GET"])
def get_ac_name():
    result = ac.get_name()
    return jsonify({"message": result})

@app.route("/ac/state", methods=["GET"])
def get_ac_state():
    result = ac.get_state()
    return jsonify({"message": result})


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5004)













































# @app.route('/ac/fan_speed', methods=['GET'])
# def fan_speed():
#     return jsonify(ac.get_action_status("fan speed"))

# @app.route('/ac/blinds_position', methods=['GET'])
# def blinds_position():
#     return jsonify(ac.get_action_status("blinds"))


# @app.route('/ac/display', methods=['GET'])
# def display():
#     return jsonify(ac.get_action_status("display"))


# @app.route('/ac/louver_angle', methods=['GET'])
# def louver_angle():
#     return jsonify(ac.get_action_status("angle"))

# @app.route('/ac/mode', methods=['GET'])
# def mode():
#     return jsonify(ac.get_action_status("mode"))
