import threading
from tkinter import Label

import cv2
import e
import numpy as np
import json
import os

from PySide6.QtGui import QImage
from sklearn.preprocessing import LabelEncoder

from FaceRecognition.face_Recognition_Training import trainer_main

class CameraDetector:
    def __init__(self, cap, frame_processed_callback):
        self.cap = cap
        self.recognizer = None
        self.frame_processed_callback = frame_processed_callback
        self.label_map = None

    def load_recognizer(self, recognizer):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))  # Needs absolute path to work.
            file_path = os.path.join(script_dir, 'trained_model.json')
            with open(file_path, 'r') as json_file:
                recognizer_data = json.load(json_file)

            recognizer.setRadius(recognizer_data["radius"])
            recognizer.setNeighbors(recognizer_data["neighbors"])
            recognizer.setGridX(recognizer_data["grid_x"])
            recognizer.setGridY(recognizer_data["grid_y"])
            recognizer.setThreshold(recognizer_data["threshold"])

            return recognizer
        except FileNotFoundError:
            print("Error: Trainer file 'trained_model.json' not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Failed to decode 'trained_model.json'.")
            return None
        except Exception as e:
            print(f"Error loading recognizer: {e}")
            return None
    #Take Attendance Function

    def convert_to_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return qt_image


    def detect_faces_from_camera(self, cap, model, labels):
        try:
            label_encoder = LabelEncoder()
            #OpenCV's pre-trained Haar Cascade Classifier for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if face_cascade.empty():
                print("Error: Failed to load Haar Cascade Classifier.")
                return
            # Open the default camera
            # cap = cv2.VideoCapture(0) #0 is the default camera
            # if not cap.isOpened():
            #     print("Error: Failed to open camera.")
            #     return
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break
                #Convert to grayscale for face detection
                gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, 1.1,4)#Detect faces

                # if len(faces)==0:
                #     print("No faces detected.")

                for (x,y,w,h) in faces:
                    #Rectangle around the face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face= gray[y:y+h, x:x+w]
                    #Normalize face for comparision
                    face_resized = cv2.resize(face, (224, 224)) #Change it so its the size of the faces in the model
                    face_normalized = face_resized / 255.0
                    face_input = np.expand_dims(face_normalized, axis=0)
                    face_input = np.expand_dims(face_input, axis=-1)

                    # Call the prediction with the model
                    prediction = model.predict(face_input)
                    pred_id = labels[np.argmax(prediction)]
                    print(f"prediction shape {prediction.shape}"
                          f"pred_id = {pred_id}"
                          f"predicted_class {np.argmax(prediction)}")
                    print(f"labels {labels}")
                    # print(f"name: {pred_id}")

                    # # Get the labels for the names
                    label_encoder.fit(labels)
                    predicted_numeric_label = pred_id  # Example: the model predicts numeric label 1
                    predicted_label = str(label_encoder.inverse_transform([predicted_numeric_label])[0])
                    # print(str(predicted_label))

                    #Recognize the face

                    # else:
                    #     label_text= "Unknown"
                    #     confidence_label = ""

                    cv2.putText(frame, predicted_label, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 2)
                    # cv2.putText(frame, confidence, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 2)

                #Press 'q' to quit.

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    #release resources
                qt_image = self.convert_to_frame(frame)
                self.frame_processed_callback(qt_image)
            cap.release()
            cv2.destroyAllWindows()


        except cv2.error as e:
            print("Error", f"OpenCV error: {e}")
        except Exception as e:
            print("Error", f"Error during detection: {e}")
            self.cap.release()
            cv2.destroyAllWindows()

    #Function to handle button click
    def start_camera(self, camera):
        # self.frame_processed_callback = frame_processed_callback
        model, labels =trainer_main()
        if model is None:
            return

        #Run face detection in a different Thread to avoid freezing
        thread=threading.Thread(target=self.detect_faces_from_camera, args=(camera,model, labels))
        thread.daemon = True
        thread.start()




