from flask import Flask, request, jsonify ,render_template
from light.light import Light  # Assuming you have a light.py file with a Light class

app = Flask(__name__)
light = Light()



# דף הבית (optional)
@app.route("/")
def home():
    return render_template("index.html")

# שינוי מצב האור
@app.route("/light/state", methods=["POST"])
def change_light_state():
    data = request.json
    state = data.get("state")
    if state is not None:
        result = light.set_state(state)
        return jsonify({"message": result})
    return jsonify({"message": "Invalid state value"}), 400

# שינוי צבע האור
@app.route("/light/color", methods=["POST"])
def change_light_color():
    data = request.json
    color = data.get("color")
    if color:
        result = light.set_color(color)
        return jsonify({"message": result})
    return jsonify({"message": "Color not specified"}), 400

# שינוי בהירות האור
@app.route("/light/brightness", methods=["POST"])
def change_light_brightness():
    data = request.json
    brightness = data.get("brightness")
    if brightness is not None:
        result = light.set_brightness(brightness)
        return jsonify({"message": result})
    return jsonify({"message": "Brightness not specified"}), 400

# שינוי בהירות האור
@app.route("/light/name", methods=["POST"])
def change_light_name():
    data = request.json
    name = data.get("name")
    if name is not None:
        result = light.change_name(name)
        return jsonify({"message": result})
    return jsonify({"message": "Brightness not specified"}), 400

# שינוי בהירות האור
@app.route("/light/increase_brightness", methods=["POST"])
def increase_light_brightness():
    data = request.json
    num = data.get("num")
    if num is not None:
        result = light.increase_brightness(num)
        return jsonify({"message": result})
    else:
        result = light.increase_brightness()
        return jsonify({"message": result})
    # return jsonify({"message": "Brightness not specified"}), 400


@app.route("/light/decrease_brightness", methods=["POST"])
def decrease_light_brightness():
    data = request.json
    num = data.get("num")
    if num is not None:
        result = light.decrease_brightness(num)
        return jsonify({"message": result})
    else:
        result = light.decrease_brightness()
        return jsonify({"message": result})
    
@app.route("/light/get_color", methods=["GET"])
def get_light_color():
    result = light.get_color()
    return jsonify({"message": result})

@app.route("/light/get_name", methods=["GET"])
def get_light_name():
    result = light.get_name()
    return jsonify({"message": result})

@app.route("/light/brightness", methods=["GET"])
def get_light_brightness():
    result = light.get_brightness()
    return jsonify({"message": result})
    
@app.route("/light/state", methods=["GET"])
def get_light_state():
    result = light.get_state()
    return jsonify({"message": result})

# הפעלת השרת
if __name__ == "__main__":
    app.run(port=4000, debug=True)