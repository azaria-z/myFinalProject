
import inflect #ספריה בשביל ההמרה  מרבים ליחיד 

#לדאוג שיכנסו רק שמות הכמויות האלה
#לדאוג לרבים (אם יש דבר כזה)

unit_conversion = {
    "tablespoon": 10,  # כף = 10 גרם
    "teaspoon": 5,      # כפית = 5 גרם
    "cup": 200,         # כוס = 200 גרם (תלוי במצרך)
    "gram": 1,          # גרם = 1 גרם 
    "ml": 1,            # מיליליטר = 1 גרם (רק למים)
}

def coculate_amount(required_amount):
        required_value, required_unit = required_amount.split()  # לדוגמה: '2 tablespoons'
        required_unit = required_unit.lower()  # המרה לאותיות קטנות
        p = inflect.engine()
        unit = p.singular_noun(required_unit)
        required_unit = unit if unit else required_unit
        amount = int(unit_conversion[required_unit])
        required_amount_in_grams = amount * int(required_value)
        return required_amount_in_grams
    