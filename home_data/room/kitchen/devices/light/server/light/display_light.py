import tkinter as tk
from tkinter import Canvas

class LightDisplay:
    def __init__(self, root, light):
        self.light = light
        self.root = root
        self.root.title("Smart Light Display")

        # כותרת
        self.label = tk.Label(root, text="Light Status", font=("Arial", 16))
        self.label.pack(pady=10)

        # ציור המנורה
        self.canvas = Canvas(root, width=200, height=300, bg="white")
        self.canvas.pack()

        # מלבן כבסיס למנורה
        self.bulb = self.canvas.create_oval(50, 50, 150, 150, fill="gray")
        self.brightness_overlay = self.canvas.create_oval(60, 60, 140, 140, fill="", outline="")

        # טקסט מידע
        self.info_label = tk.Label(root, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)

        self.update_display()

    def update_display(self):
        status = self.light.get_state()
        color = self.light.get_color().lower()
        brightness = self.light.get_brightness()

        # עדכון צבע
        fill_color = color if status else "gray"
        self.canvas.itemconfig(self.bulb, fill=fill_color)

        # סימולציה של שקיפות לפי עוצמה
        brightness_hex = hex(int(255 * (brightness / 100)))[2:].zfill(2)
        overlay_color = f"#{brightness_hex * 3}"
        self.canvas.itemconfig(self.brightness_overlay, fill=overlay_color if status else "")

        # טקסט
        text = f"Status: {'On' if status else 'Off'}\nColor: {color}\nBrightness: {brightness}%"
        self.info_label.config(text=text)


