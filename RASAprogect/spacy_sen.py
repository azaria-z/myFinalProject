# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"


import spacy

nlp = spacy.load("en_core_web_sm")

def extract_action(text):
    doc = nlp(text.lower())
    v=[]
    for token in doc:
        # print(token.text, token.dep_, token.head.text, token.head.pos_)
        if token.dep_ == "prt" and token.head.pos_ == "VERB":
            return f"{token.head.text} {token.text}"  # למשל: turn on
        if token.pos_ == "VERB":
            v.append(token.text)  # פועל רגיל אם אין particle
    return v[0] if v else None  # אם לא נמצא פועל עם particle, מחזירים את הפועל הרגיל

