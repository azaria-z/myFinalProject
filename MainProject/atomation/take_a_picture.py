

import cv2
from datetime import datetime
import os

def capture_image():
    # פותח את המצלמה
    cap = cv2.VideoCapture(0)

    # בדיקה שהמצלמה נפתחה
    if not cap.isOpened():
        print("Cannot open the camera")
        return None

    # קריאת פריים יחיד (תמונה אחת)
    ret, frame = cap.read()
    image_path = None

    if ret:
        # יצירת שם קובץ עם תאריך ושעה
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        directory = "D:\\temp\\Documents\\project\\Text analysis\\home_data\\picture_project"

        # יצירת התיקייה אם לא קיימת
        os.makedirs(directory, exist_ok=True)

        # שמירת התמונה
        image_path = os.path.join(directory, filename)
        cv2.imwrite(image_path, frame)
        print(f"Image saved at: {image_path}")
    else:
        print("Failed to read image")

    # שחרור המצלמה
    cap.release()

    return image_path

























































# if __name__ == "__main__":
    
#     path = capture_image()
#     if path:
#         print("The system will continue with facial recognition according to:", path)
#     else:
#         print("Cannot continue - no image taken.")
    
















