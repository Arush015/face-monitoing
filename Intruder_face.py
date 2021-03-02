import cv2
face_cascade=cv2.CascadeClassifier(r'C:\Users\Admin\PycharmProjects\opencv\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

def detect(grey,frame):
    faces=face_cascade.detectMultiScale(grey,1.3,5)
    for (x,y,w,h)in faces :
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)
        roi_grey=grey[y:y+h, x:x+w]
        roi_color=frame[y: y+h, x:x+w]
    return frame

camera = cv2.VideoCapture(0)
i=1
while i>0:
    return_value, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converting to grayscale.
    canvas = detect(gray, frame)
    cv2.imshow('intruder.png',canvas)
    i=i-1
cv2.waitKey(0)
del(camera)