import cv2
import numpy as np
import pygame
import tkinter as tk
from tkinter import ttk

pygame.init()
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound('alarm.mp3')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

def start_drowsiness_detection():
    global alarm_playing
    closed_eyes_timer = 0
    eyes_closed = False
    alarm_playing = False

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            if len(eyes) == 0:
                closed_eyes_timer += 1
                if closed_eyes_timer >= 125:
                    eyes_closed = True
                    if not alarm_playing:
                        alarm_sound.play()
                        alarm_playing = True
                cv2.putText(frame, "Eyes Closed", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                closed_eyes_timer = 0
                eyes_closed = False
                if alarm_playing:
                    alarm_sound.stop()
                    alarm_playing = False
                cv2.putText(frame, "Eyes Open", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Drowsiness Detection', frame)

        key = cv2.waitKey(1)
        if key == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()
    alarm_sound.stop()  


def stop_alarm():
    alarm_sound.stop()

root = tk.Tk()
root.title("Drowsiness Detection App")

label = ttk.Label(root, text="Drowsiness Detection App")
label.pack(pady=10)

start_button = ttk.Button(root, text="Start Detection", command=start_drowsiness_detection)
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop Alarm", command=stop_alarm)
stop_button.pack(pady=10)

root.mainloop()
