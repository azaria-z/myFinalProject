from flask import Flask, request, jsonify,render_template
from coffee_machine.coffee_machine import Coffee_Machine

app = Flask(__name__)

# יצירת מופע אחד של מכונת הקפה
coffee_machine = Coffee_Machine()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/CM/state', methods=["POST"])
def change_CM_state():
    data = request.json
    state = data.get("state")
    if state is not None:
        result = coffee_machine.set_state(state)
        return jsonify({"message": result})
    return jsonify({"message": "Invalid state value"}), 400

#הוספת מרכיב
@app.route("/CM/ingredient/increase", methods=["POST"])
def add_ingredient():
    data = request.json
    name = data.get("ingredient")
    amount = data.get("amount", 0)
    amount= int(amount) if isinstance(amount, str) and amount.isdigit() else amount
    result = coffee_machine.add_ingredient(name, amount)
    return jsonify({"message": result})

# הסרת מרכיב
@app.route("/CM/ingredient/decrease", methods=["POST"])
def remove_ingredient():
    data = request.json
    name = data.get("ingredient")
    amount = data.get("amount", 0)
    amount= int(amount) if isinstance(amount, str) and amount.isdigit() else amount
    result = coffee_machine.reduce_ingredients(name, amount)
    return jsonify({"message": result})



@app.route("/CM/make_coffee", methods=["POST"])
def make_coffee():
    data = request.json
    coffee = data.get("coffee","regular")
    result = coffee_machine.make_coffee(coffee)
    return jsonify({"message": result})

@app.route("/CM/coffee/types", methods=["GET"])
def get_coffee_types():
    return jsonify(coffee_machine.get_coffee_types())

@app.route("/CM/<coffee_type>/ingredients", methods=["GET"])
def get_coffee_ingredients(coffee_type):
    try:
        result = coffee_machine.get_coffee_ingredient(coffee_type)
        return result
    except:
        return jsonify({"error": "Invalid coffee type"}), 400

@app.route("/CM/ingredients", methods=["GET"])
def get_ingredients_status():
    return jsonify(coffee_machine.get_ingredients_status())

@app.route("/CM/ingredients_JSON", methods=["GET"])
def get_ingredients_json():
    return jsonify(coffee_machine.get_ingredients_json())

@app.route("/CM/ingredient/<name>", methods=["GET"])
def get_ingredient(name):
    result = coffee_machine.get_ingredient(name)
    return jsonify({"message": result})

@app.route("/CM/state", methods=["GET"])
def get_state():
    return jsonify({"state": coffee_machine.get_state()})


if __name__ == "__main__":
    app.run(debug=True, port= 5006)
