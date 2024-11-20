import threading
import cv2
import e
import numpy as np
import json
import os
from FaceRecognition.face_Recognition_Training import trainer_main

class CameraDetector:
    def __init__(self, cap):
        self.cap = cap
        self.recognizer = None

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
            # recognizer.read("trained_model.yml") #Ensure compatibility if LBPH model is separately stored
            # Check if recognizer was trained
            # if not recognizer_data.get("faces") or not recognizer_data.get("labels"):
            #     print("Error: No training data found. Re-training...")
            #     trainer_main()
            #     print("Training complete. Restart the application.")
            #     return None
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

    def detect_faces_from_camera(self, recognizer, cap):
        try:
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

                if len(faces)==0:
                    print("No faces detected.")

                for (x,y,w,h) in faces:
                    #Rectangle around the face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face= gray[y:y+h, x:x+w]
                    #Recognize the face
                    label, confidence=recognizer.predict(face)
                    print(confidence)
                    if confidence <100:
                        label_text= f"ID {label}, Conf: {round(confidence,2)}"
                        #record_attendance (label) #record attendance for recognized face
                    else:
                        label_text= "Unknown"

                    cv2.putText(frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 2)
                cv2.imshow('Face Detection', frame)

                #Press 'q' to quit.

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    #release resources
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
        recognizer= trainer_main()
        if recognizer is None:
            return

        #Run face detection in a different Thread to avoid freezing
        thread=threading.Thread(target=self.detect_faces_from_camera, args=(recognizer,camera))
        thread.start()
#MAIN
# def main():
#     print("Starting live face detection...")
#     self.start_camera()


# if __name__ == "__main__":
#     main()




