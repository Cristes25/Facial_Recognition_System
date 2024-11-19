import threading

import cv2
import e
import numpy as np
import json
import os

class CameraDetection:
    def __init__(self, cap):
        self.cap = cap

    def load_recognizer(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__)) # Needs absolute path to work.
            file_path = os.path.join(script_dir, 'trained_model.json')
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
            with open(file_path, 'r') as json_file:
                recognizer = json.load(json_file)
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.setRadius(recognizer["radius"])
            recognizer.setNeighbors(recognizer["neighbors"])
            recognizer.setGridX(recognizer["grid_x"])
            recognizer.setGridY(recognizer["grid_y"])
            recognizer.setThreshold(recognizer["threshold"])
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

    def detect_faces_from_camera(self, recognizer, cap):
        print("Calls detect faces")
        try:
            print("Got into the try")
            #OpenCV's pre-trained Haar Cascade Classifier for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if face_cascade.empty():
                print("Error: Failed to load Haar Cascade Classifier.")
                return
            # #This is done in the camera.py
            # # Open the default camera
            # cap = cv2.VideoCapture(0) #0 is the default camera
            # if not cap.isOpened():
            #     print("Error: Failed to open camera.")
            #     return
            while True:
                print("HERE!")
                ret, frame = cap.isOpened()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break
                #Convert to grayscale for face detection
                gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray, 1.1,4)#Detect faces

                if len(faces)==0:
                    print("No faces detected.")

                for (x,y,w,h) in faces:
                    #Rectangle around the face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face= gray[y:y+h, x:x+w]
                    label, confidence=recognizer.predict(face)
                    if confidence <100:
                        label_text= f"ID {label}, Conf: {round(confidence,2)}"
                    else:
                        label_text= "Unknown"
                    cv2.putText(frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 2)
                cv2.imshow('Face Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        except cv2.error as e:
            print("Error", f"OpenCV error: {e}")
        except Exception as e:
            print("Error", f"Error during detection: {e}")
            cap.release()
            cv2.destroyAllWindows()

    #Function to handle button click
    def start_camera(self, cap):
        self.recognizer = self.load_recognizer()
        if self.recognizer is None:
            print("problem is with recognizer")
            return

        self.detect_faces_from_camera(self.recognizer, cap)

        #Run face detection in a different Thread to avoid freezing
        # thread=threading.Thread(target=self.detect_faces_from_camera, args=(self.recognizer,self.cap))
        # thread.start()