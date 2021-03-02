import face_recognition
import io
import sqlite3
import cv2
import base64
import datetime

conn = sqlite3.connect('Dataset.db')
cursor = conn.cursor()
video_capture = cv2.VideoCapture(0)

known_face_encodings = []
names = []
cursor.execute('Select * from face;')
data = cursor.fetchall()
for i in data:
    name = i[1]
    names.append(name)
for i in range(len(data)):
    data1 = base64.b64decode(data[i][2])
    file_like = io.BytesIO(data1)

    image = face_recognition.load_image_file(file_like)
    #face_recognition.api.load_image_file(file, mode='RGB')
    #Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    
    face_encoding = face_recognition.face_encodings(image)[0]
    #face_recognition.api.face_encodings(face_image, known_face_locations=None, num_jitters=1, model='small')
    #Returns: A list of 128-dimensional face encodings (one for each face in the image)
    
    known_face_encodings.append(face_encoding)

face_locations = []
face_encodings = []
process_this_frame = True

while True:

    # Grabbing a single frame at a time
    ret, frame = video_capture.read()
    timestamp = datetime.datetime.now()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color to RGB color
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)
        #face_recognition.api.batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128)
        #Returns: A list of tuples of found face locations in css (top, right, bottom, left) order
        
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        #face_recognition.api.face_encodings(face_image, known_face_locations=None, num_jitters=1, model='small')
        #Returns: A list of 128-dimensional face encodings (one for each face in the image)
        
        face_names = []
        for face_encoding in face_encodings:
        
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            #face_recognition.api.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6)
            #Returns: A list of True/False values indicating which known_face_encodings match the face encoding to check
            
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = names[first_match_index]
            face_names.append(name)
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # cv2.rectangle(frame, (10, frame.shape[0] - 10), (10, frame.shape[0] - 10), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        ts = timestamp.strftime("%d %B, %Y %I:%M:%S%p")
        if name == 'Unknown':
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)
        else:
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), font, 0.75, (255, 255, 255), 1)
    cv2.imshow('Video', frame)

    # Hit q to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
conn.commit()
cursor.close()
conn.close()
