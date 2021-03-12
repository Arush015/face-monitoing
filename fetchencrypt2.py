import cv2
import sqlite3
from cryptography.fernet import Fernet
import time

start_time = time.time()
use = input("Enter Name: ")
idt = input("Enter ID: ")

start_time = time.time()
face_cascade = cv2.CascadeClassifier(r'D:\Arush\PycharmProjects\CompVis\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
conn = sqlite3.connect('Dataset.db')
cursor = conn.cursor()
camera = cv2.VideoCapture(0)

for i in range(15):
    return_value, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    for (x, y, w, h) in faces:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.5, 5)
        cv2.imwrite(str(idt)+'.png', gray[y:y+h, x:x+w])

with open(str(idt)+'.png', 'rb') as data:
    photo = data.read()

with open("key.txt","rb") as file_b:
    key = file_b.read()

cipher = Fernet(key)
encodestring = cipher.encrypt(photo)
cursor.execute("INSERT INTO faces VALUES(?,?,?);", (idt, use, encodestring))

end_time = time.time() - start_time
print("Time taken: ", end_time)

del camera
conn.commit()
cursor.close()
conn.close()
cv2.waitKey(0)
