import face_recognition
import cv2
from scipy.spatial import distance as dist
import playsound
from threading import Thread
import numpy as np


MIN_AER = 0.30
EYE_AR_CONSEC_FRAMES = 10
COUNTER = 0
ALARM_ON = False


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def sound_alarm(alarm_file):
    playsound.playsound(alarm_file)


def main():
    global COUNTER
    global ALARM_ON
    video_path = 'anshikha.mp4'
    video_capture = cv2.VideoCapture(video_path)

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        face_landmarks_list = face_recognition.face_landmarks(frame)
        for face_landmark in face_landmarks_list:
            leftEye = face_landmark['left_eye']
            rightEye = face_landmark['right_eye']
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2
            lpts = np.array(leftEye)
            rpts = np.array(rightEye)
            cv2.polylines(frame, [lpts], True, (255, 255, 0), 1)
            cv2.polylines(frame, [rpts], True, (255, 255, 0), 1)
            if ear < MIN_AER:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True
                        t = Thread(target=sound_alarm,
                                   args=('alarm.wav',))
                        t.deamon = True
                        t.start()
                    cv2.putText(frame, "ALERT! You are feeling asleep!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                ALARM_ON = False
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (500, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Sleep detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
