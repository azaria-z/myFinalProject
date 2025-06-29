import speech_recognition as sr
import pyttsx3 as tts
import tkinter as tk
import threading
import requests


#פה אני מפעילה את העוזרת הקולי שלי ע"י יצירת מופע

class Assistant:

    def __init__(self):

        self.recognizer = sr.Recognizer()#שומע
        self.speaker = tts.init()#מדבר
        self.speaker.setProperty("rate", 170)#המהירות של העוזרת ככל שהיא יותר גבוהה יותר מהר
        voices= self.speaker.getProperty('voices')#קבלת הקולות
        self.speaker.setProperty("voice",voices[1].id)#לשים קול של בת
        self.listening_mode = False
        #פה יש את הממשק הגרפי לנטחות המשתמש לראות שנינה שומעת אותי
        self.root = tk.Tk()
        self.label = tk.Label(text="😁", font=("Arial", 120, "bold"))
        self.label.pack()
        self.transcript_label = tk.Label(text="", font=("Arial", 18))#הטרסט הנוסף
        self.transcript_label.pack()

        threading.Thread (target=self.run_assistant).start()#מריצה את קול העוזרת בתהליכון כדי להפריד את הממשק הגרפי
        self.root.mainloop()# הפעלת הממשק הגרפי


    

    def send_to_rasa(self, message):
        payload = {"sender": "user", "message": message}
        try:
            print("send a request")
            r = requests.post("http://localhost:5005/webhooks/rest/webhook", json=payload)
            print(r.text)
            # responses = r.json()
            # return " ".join([resp.get("text", "") for resp in responses])
            return r.json()[0]["text"] if r.status_code == 200 and r.json() else "No response"

        except Exception as e:
            print(f"Error contacting Rasa: {e}")
            return "Sorry, I couldn't reach Rasa."
        
    def shutdown(self):
        self.speaker.stop()
        self.root.quit()  # מסיים את ה-mainloop
        self.root.destroy()  # סוגר את החלון

    #העוזרת מתחילה בלהאזין לפקודות
    def run_assistant(self):
            try:
                with sr.Microphone() as mic:
                    while True:#??
                        try:
                            print("Listening for 'NINA'...")
                            # שמירה על רגישות בזמן האזנה, עם שיפור בהפחתת רעש
                            self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = self.recognizer.listen(mic)
                            # זיהוי הדיבור עם גוגל
                            text = self.recognizer.recognize_google(audio)
                            text = text.lower()
                            # print(f"Recognized: {text}")
                            # self.label.config(text=f"Recognized: {text}")
                            self.transcript_label.config(text=f"You said: {text}")
                            if "nina" in text:#קרא לעוזרת 
                                self.label.config(fg="pink")#הופכים את התגית לאדומה
                                self.speaker.say("Yes, I'm here. How can I help?")
                                self.speaker.runAndWait()#ממתינה למשימה
                                while True:
                                    try:
                                        self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                                        audio = self.recognizer.listen(mic)
                                        text = self.recognizer.recognize_google(audio)
                                        text = text.lower()

                                        # print(f"Recognized: {text}")
                                        self.transcript_label.config(text=f"You said: {text}")
                                        if "bye" in text:
                                            self.speaker.say("Bye")
                                            self.speaker.runAndWait()
                                            self.label.config(fg="black")
                                            break

                                        response = self.send_to_rasa(text)
                                        if response is not None:
                                            self.speaker.say (response)
                                            self.speaker.runAndWait()

                                    except sr.WaitTimeoutError:
                                        # היה שקט - פשוט לא מגיבים
                                        print("Silence detected – no speech")
                                        pass
                                    
                                    except sr.UnknownValueError:
                                        self.recognizer = sr.Recognizer()
                                        self.speaker.say("I did not understand you! Please try again!")
                                        self.speaker.runAndWait()
                                  
                                    except KeyboardInterrupt:
                                        print("Listening stopped by user (Ctrl+C)")
                                        self.shutdown()
                                        return
                        except sr.UnknownValueError:
                            print("Could not understand wake word")
                        except KeyboardInterrupt:
                            print("Stopped by user")
                            self.shutdown()
                            return
                        except Exception as e:
                            print(f"Outer loop error: {e}")
                            self.speaker.say("An error occurred. Restarting listening...")
                            self.label.config(fg="black")
                            self.speaker.runAndWait()
                        
                      
            except KeyboardInterrupt:
                                print("Listening stopped by user (Ctrl+C)")
                                self.shutdown()
                                return


                   
if __name__ == "__main__":
    Assistant()



# Assistant()
#מחר יש לבדוק את הקוד הזה ולראות איך אני מחברת אותו לעוזרת
#להגגדיר את זמן הריצה של הלולאה



#  self.root.destroy()
# sys.exit()
# self.speaker.stop()

# except recognizer.UnknownValueError:
#                         print("Could not understand the audio")
#                         self.label.config(fg="black")
#                         continue
#                     except recognizer.RequestError as e:
#                         print(f"Could not request results; {e}")
#         except KeyboardInterrupt:
#             print("Listening stopped by user (Ctrl+C)")
#             self.speaker.stop()
#             self.root.destroy()
                    
  # except Exception as e:
                                    #     print(f"Listening failed: {e}")
                                    #     continue