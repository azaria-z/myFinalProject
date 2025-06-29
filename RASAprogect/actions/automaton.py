from .vertex import Vertex

# #בניית האוטומט
# OUTO=Vertex()
class Automation():
        def __init__(self):
            self.OUTO=Vertex()
        #פונקציה שמוסיפה מילה לאוטומט
        def add(self, word, translate):
            v= self.OUTO
            i = 0
            while i < len(word):
                if word[i] != ' ':  
                    if not v.find_edge(word[i]):#אם אין אות כזאת
                        index = ord(word[i]) - ord('a')#יצירת אות חדשה
                        v.child[index]=Vertex()
                    if i==len(word)-1:#האות האחרונה
                        v=v.get_child(word[i])
                        if v.state:
                            if v.translate[0] != None:
                                print("The word already exists and its meaning is:"+v.translate[0])
                                return
                            else:
                                v.translate[0]=translate
                                print("The word was inserted successfully")
                            return
                        else:
                            v.state=True
                            v.translate[0]=translate
                            print("The word was inserted successfully")
                    else:
                        if word[i+1]==' ':#האות האחרונה של המילה
                            v=v.get_child(word[i])
                            if i+2 < len(word):
                                v.continue_search.append(word[i+2:])#מכניס את המשך המילה לחיפוש
                                i+=1
                        else:
                            v=v.get_child(word[i])
                i+=1



        #פונקציה שמדפיסה את המילים האוטומט
        def print_outo(self, word):
            is_leaf = True
            for i in range(0, 26):
                if self.OUTO.child[i] is not None:
                    self.print_outo(self.OUTO.child[i], word + chr(i + ord('a')))
                    is_leaf = False
            if is_leaf or self.OUTO.state:
                print(word)


        def search(self,word):
            v=self.OUTO
            i = 0
            while i < len(word):
                if word[i] != ' ':
                    if not v.find_edge(word[i]):
                        print ("The word does not exist")
                        return None
                    v=v.get_child(word[i])
                    if i==len(word)-1:
                        if v.state:
                            if v.translate[0] != None:
                                 print("The meaning of the word is:"+v.translate[0])
                                 return v.translate[0]
                            else:
                                print ("The word does not exist")
                                return None
                        else:
                            if len(v.continue_search) > 0:
                                for j in range(0,len(v.continue_search)):
                                    print(v.continue_search[j])
                                word= input("Enter the continuation of the word:")
                                i=-1
                            else:
                                print ("The word does not exist")
                                return None
                i+=1
            print ("The word does not exist")
            return None
       
      