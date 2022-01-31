"""@author: k@author: Robert Amoot
"""
# Face Recognition

# Importing the libraries
import time

from PIL import Image
from keras.applications.vgg16 import preprocess_input
import base64
from io import BytesIO
import json
import random
import cv2
from keras.models import load_model
import numpy as np
from attend import Attend

from keras.preprocessing import image

model = load_model('facefeatures_new_model.h5')
attend = Attend()

# Loading the cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

from glob import glob

class_names = glob("assets/images/*")  # Reads all the folders in which images are present
class_names = sorted(class_names)  # Sorting them
my_classes = dict(zip(range(len(class_names)), class_names))
print(my_classes)


def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns the input image

    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.3, 5)

    if faces is ():
        return None

    # Crop all faces found
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cropped_face = img[y:y + h, x:x + w]

    return cropped_face


class LiveCam:
    def get_feed(self):
        # Doing some Face Recognition with the webcam
        video_capture = cv2.VideoCapture(0)
        while True:
            _, frame = video_capture.read()
            # canvas = detect(gray, frame)
            # image, face =face_detector(frame)

            face = face_extractor(frame)
            if type(face) is np.ndarray:
                face = cv2.resize(face, (224, 224))
                im = Image.fromarray(face, 'RGB')
                # Resizing into 128x128 because we trained the model with this image size.
                img_array = np.array(im)
                # Our keras model used a 4D tensor, (images x height x width x channel)
                # So changing dimension 128x128x3 into 1x128x128x3
                img_array = np.expand_dims(img_array, axis=0)
                pred = model.predict(img_array)
                print(pred)

                name = f'{str(time.localtime().tm_hour)}:{str(time.localtime().tm_min)}:{str(time.localtime().tm_sec)}'

                i = 0
                class_count = len(my_classes)
                print(class_count)

                for class_t in my_classes:
                        # my_classess[i] gives the folder name for the current image
                    try:
                        if pred[0][i] > 0.5 and i<class_count:
                            picture = frame.tolist()
                            employee_id = (my_classes[i]).replace('assets/images\\', '')
                            print(f'Prediction for {employee_id} {pred[0][i]}')
                            attend.capture(int(employee_id), picture)
                    except:
                        print('Camera Error')
                    i = i + 1

                # attend.take_attendance(face)

                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else:
                print('No faces')
                #cv2.putText(frame, "", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                # cv2.imshow('Video', frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #   break
        video_capture.release()
        cv2.destroyAllWindows()
