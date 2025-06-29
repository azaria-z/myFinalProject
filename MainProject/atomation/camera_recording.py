

#הסרטה של מצלמה
import datetime

import cv2
import threading
import time
import os
# משתנים גלובליים
cap = None
writer = None
recording = False
recording_thread = None

def _record_loop():
    global cap, writer, recording

    while recording:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Recording", frame)
        writer.write(frame)

        # מאפשר לסגור את החלון בלחיצה על X
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print("Recording finished.")

def start_recording(width=1280, height=720, fps=30.0):
    direction = "D:\\temp\\Documents\\project\\Text analysis\\home_data\\video"
    if not os.path.exists(direction):
        os.makedirs(direction)
    filename = datetime.datetime.now().strftime("recording_%Y-%m-%d_%H-%M-%S.mp4")
    filepath = os.path.join(direction, filename)
    global cap, writer, recording, recording_thread

    if recording:
        print("Recording is already active.")
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    recording = True
    recording_thread = threading.Thread(target=_record_loop)
    recording_thread.start()

    print("Starting recording...")

def stop_recording():
    global recording, recording_thread

    if not recording:
        print("Recording is not active.")
        return

    recording = False
    recording_thread.join()  # מחכה שיסיים
    print("Recording has stopped.")

# if __name__ == "__main__":
#     start_recording()       # מתחיל להקליט ולהציג את המסך
#     time.sleep(3)  # import time
#     # לאחר כמה שניות או כתלות בתנאי
#     stop_recording()        # מפסיק את ההקלטה וסוגר את המסך






# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# writer = cv2.VideoWriter("recording.mp4", fourcc, 30.0, (1280, 720))

# recording = False

# while True:
# 	ret, frame = cap.read()
# 	if ret:
# 		cv2.imshow("video", frame)
# 		if recording:
# 			writer.write(frame)
# 	# Add a break condition to exit the loop, e.g., pressing 'q'
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break

# cap.release()
# writer.release()
# cv2.destroyAllWindows()