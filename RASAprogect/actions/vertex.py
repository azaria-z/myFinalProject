
#מחלקה שמתארת מצב מקבל
#אם מאגר המילים מכיל את האפשרויות להמשכה חיפוש הגרף
class Vertex:
    def __init__(self):
        self.state =False
        self.continue_search =[]#במקרה של ביטיו יש לו המשך
        self.translate=[None] * 2 #האם  זה פועל או ש"ע: מקום 1= פועל 2=ש"ע
        self.child = [None] * 26  #מערך של ילדים

    #פונקציה שמקבלת משפט ובודקת אם מופיעה בו אחד מהמילים במאגר
    #הפיתרון שכתבתי פה מאוד נאיבי צריך למצוא פיתרון יותר יעיל
    def find_edge(self, letter):
        index = ord(letter.lower()) - ord('a')  # ממיר את האות לאינדקס בין 0 ל-25
        return self.child[index] is not None  # בדיקה אם קיים צומת לאות זו

    def get_child(self, letter):
        index = ord(letter.lower()) - ord('a')  # ממיר את האות לאינדקס בין 0 ל-25
        return self.child[index]

    