import hashlib
import threading
import time
from tkinter import Label

import cv2
import e
import numpy as np
import json
import os
import tensorflow as tf

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage
from multiprocessing import Queue

import pickle

from FaceRecognition.face_Recognition_Training import trainer_main

class CameraDetector:
    def __init__(self, cap, frame_processed_callback):
        self.cap = cap
        self.recognizer = None
        self.frame_processed_callback = frame_processed_callback
        self.last_emit_time = time.time()
        self.emit_interval = 0.05
        self.running = True
        self.encoder = self.load_encoder()
        self.known_face_hashes = {}
        self.face_queue = Queue(maxsize=10)  # Queue for detected faces

    def load_encoder(self, file_name='label_encoder.pkl'):
        '''
        Previous function deleted. Para mandar a llamar los nombres necesita el mismo enconder con el que se codificaron
        La creacion del encoder esta en el archivo del trainer. Antes lo pasaba como argumento entre funciones pero esta manera es mas segura
        '''
        try:
            with open(file_name, 'rb') as f:
                label_encoder = pickle.load(f)
            print(f"LabelEncoder loaded from {file_name}")
            return label_encoder
        except Exception as e:
            print(f"Error loading LabelEncoder: {e}")
            return None

    def convert_to_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return qt_image


    def hash_face(self, face_image):
        '''Create a unique hash for each face image based on its content.'''
        image_hash = hashlib.md5(face_image.tobytes()).hexdigest()
        return image_hash

    def detect_all_faces(self, cap):
        '''Detect faces in the video stream and add them to the queue.'''
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if face_cascade.empty():
                print("Error: Failed to load Haar Cascade Classifier.")
                return

            last_detection_time = time.time()

            while self.running:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if not ret or frame is None:  # Check if frame is valid
                    print("Warning: Failed to capture frame. Retrying...")
                    continue

                # Added this to control the frame rate
                current_time = time.time()
                if current_time - last_detection_time < 0.05:
                    continue

                last_detection_time = current_time
                faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(150, 50), maxSize=(350, 350))

                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        face = gray[y:y + h, x:x + w]

                        # Normalize and resize face for the model
                        face_resized = cv2.resize(face, (240, 240))
                        face_normalized = face_resized / 255.0
                        face_input = np.expand_dims(face_normalized, axis=0)
                        face_input = np.expand_dims(face_input, axis=-1)

                        # Add face to the queue for prediction
                        face_hash = self.hash_face(face_input)
                        if face_hash not in self.known_face_hashes:
                            self.face_queue.put(face_input)
                            self.known_face_hashes[face_hash] = {"Confidence": 0.0, "Predicted": False}

                qt_image = self.convert_to_frame(frame)
                self.frame_processed_callback(qt_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False

            cap.release()
            cv2.destroyAllWindows()

        except cv2.error as e:
            print("Error", f"OpenCV error: {e}")
        except Exception as e:
            print("Error", f"Error during detection: {e}")
            self.cap.release()
            cv2.destroyAllWindows()

    def predict_faces(self, model):
        '''Process the faces in the queue and make predictions.'''
        while self.running:
            try:
                if not self.face_queue.empty():
                    while not self.face_queue.empty():
                        face = self.face_queue.get()
                        prediction = model.predict(face)

                        predicted_label = str(np.argmax(prediction))
                        confidence = round(float(np.max(prediction)), 2)

                        if predicted_label not in self.known_face_hashes:
                            self.known_face_hashes[predicted_label] = {
                                "Confidence": 0.0, "Predicted": False}

                        # Update the known face hashes if confidence is high enough
                        if confidence >= 0.03 and not self.known_face_hashes[predicted_label]["Predicted"]:
                            self.known_face_hashes[predicted_label]["Confidence"] = confidence
                            self.known_face_hashes[predicted_label]["Predicted"] = True

                        elif confidence > self.known_face_hashes[predicted_label]["Confidence"]:
                            # Update confidence if it improves
                            self.known_face_hashes[predicted_label]["Confidence"] = confidence

                        print(f"Predicted label: {predicted_label}, confidence: {confidence}")

                time.sleep(0.05)  # Prevent slowdown

            except Exception as e:
                print(f"Exception on predict_faces {e}")

    def start_camera(self, camera):
        encoder = trainer_main()
        model = tf.keras.models.load_model('face_recognition_model.keras')
        if model is None:
            return
        # Run face detection and prediction in separate threads
        detection = threading.Thread(target=self.detect_all_faces, args=(camera,))
        detection.daemon = True

        prediction = threading.Thread(target=self.predict_faces, args=(model,))
        prediction.daemon = True

        detection.start()
        time.sleep(1)  # Give some time for camera to initialize
        prediction.start()


# class CameraDetector:
#     def __init__(self, cap, frame_processed_callback):
#         self.cap = cap
#         self.recognizer = None
#         self.frame_processed_callback = frame_processed_callback
#         self.last_emit_time = time.time()
#         self.emit_interval = 0.05
#         self.running = True
#         self.encoder = self.load_encoder()
#         self.known_face_hashes = {}
#         self.face_queue = Queue(maxsize=10)  # Todas las caras q se detectan (y no se han analizado) se registran aqui
#         # para ir haciendo la prediccion.
#
#     def load_encoder(self, file_name='label_encoder.pkl'):
#         '''
#         Previous function deleted. Para mandar a llamar los nombres necesita el mismo enconder con el que se codificaron
#         La creacion del encoder esta en el archivo del trainer. Antes lo pasaba como argumento entre funciones pero esta manera es mas segura
#         '''
#         try:
#             with open(file_name, 'rb') as f:
#                 label_encoder = pickle.load(f)
#             print(f"LabelEncoder loaded from {file_name}")
#             return label_encoder
#         except Exception as e:
#             print(f"Error loading LabelEncoder: {e}")
#             return None
#
#     def convert_to_frame(self, frame):
#         rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#         return qt_image
#
#     def hash_face(self, face_image):
#         '''Crea un codigo unico para cada cara, si la cara ya fue detectada, se pone alguien nuevo enfrente y es diferente
#         obliga al codigo a ejecutar otra prediccion. Unica manera de solucionar el problema de que se quedaba estancado en una
#         sola cara
#         '''
#         image_hash = hashlib.md5(face_image.tobytes()).hexdigest()
#         return image_hash
#
#     def detect_all_faces(self, cap):
#         '''Reciclado de las primeras versiones. Detecta las caras en el frame. Las agrega a una queue y crea el hash aqui'''
#         try:
#             #OpenCV's pre-trained Haar Cascade Classifier for face detection
#             face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#             if face_cascade.empty():
#                 print("Error: Failed to load Haar Cascade Classifier.")
#                 return
#             last_detection_time = time.time()
#
#             while self.running:
#                 ret, frame = cap.read()
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 if not ret or frame is None:  # Check if frame is valid
#                     print("Warning: Failed to capture frame. Retrying...")
#                     continue
#
#                 # Added this so it runs at 20 fps, to avoid the prediction falling behind
#                 current_time = time.time()
#                 if current_time - last_detection_time < 0.05:
#                     continue
#
#                 last_detection_time = current_time
#                 faces = face_cascade.detectMultiScale(gray, 1.1,4, minSize=(150,50), maxSize=(350,350))#Detect faces
#
#                 # To check the faces are being detected correctly
#                 # for i, (x, y, w, h) in enumerate(faces):
#                 #     face_debug = gray[y:y + h, x:x + w]
#                 #     cv2.imshow(f"Face {i + 1}", face_debug)
#                 #     cv2.waitKey(1)
#                 if len(faces) > 0:
#                     for (x, y, w, h) in faces:
#                         # Rectangle around the face
#                         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                         face = gray[y:y + h, x:x + w]
#
#                         # Normalize face for comparison
#                         face_resized = cv2.resize(face, (240, 240))  # Change it so it's the size of the faces in the model
#                         face_normalized = face_resized / 255.0
#                         face_input = np.expand_dims(face_normalized, axis=0)
#                         face_input = np.expand_dims(face_input, axis=-1)
#                         # Put face into the queue for prediction
#                         self.face_queue.put(face_input)
#
#                 qt_image = self.convert_to_frame(frame)
#                 self.frame_processed_callback(qt_image)
#
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 self.running = False
#
#             cap.release()
#             cv2.destroyAllWindows()
#
#         except cv2.error as e:
#             print("Error", f"OpenCV error: {e}")
#         except Exception as e:
#             print("Error", f"Error during detection: {e}")
#             self.cap.release()
#             cv2.destroyAllWindows()
#
#     def predict_faces(self, model):
#         ''' Revisa las caras en la queue que se agregaron en la funcion anterior.'''
#         while self.running:
#             try:
#                 if not self.face_queue.empty():
#                     while not self.face_queue.empty():
#                         face = self.face_queue.get()
#                         # print(face_hash)
#                         # if not self.known_face_hashes[face_hash]["Predicted"]:
#                         prediction= model.predict(face)
#
#                         # TODO hacer el hash basado en la prediccion. Es necesario el bash? (No es)
#                         predicted_label = str(self.encoder.classes_[np.argmax(prediction)])
#                         self.known_face_hashes[predicted_label] = {"Confidence": 0.0,
#                                                                    "Predicted": False}
#
#                         confidence = round(float(np.max(prediction)), 2)
#
#                         if confidence < 0.02:
#                             del self.known_face_hashes[predicted_label]
#
#                         if confidence > 0.03 and not self.known_face_hashes[predicted_label]["Predicted"]: # Add it as predicted only if there is a high confidence (Currently edited with the max confidence we get)
#                             self.known_face_hashes[predicted_label]["Confidence"] = confidence
#                             self.known_face_hashes[predicted_label]["Predicted"] = True
#                             print(self.known_face_hashes[predicted_label])
#
#                         elif confidence > self.known_face_hashes[predicted_label]["Confidence"]:
#                             print(self.known_face_hashes[predicted_label]["Confidence"])
#                             self.known_face_hashes[predicted_label]["Confidence"] = confidence
#
#                         print(f"Predicted label = {predicted_label}, confidence {confidence}") # Ya no se muestra sobre la cabeza, no es necesario
#                         print(self.known_face_hashes)
#                         # TODO lo que se guarde aqui seria lo que se use para llenar los reportes
#                         # print(f"Prediction for face {i + 1}: {label_encoder.classes_[np.argmax(prediction)]} with confidence {max(prediction):.2f}")
#
#                 time.sleep(0.05) # Para evitar q se lentee
#             except Exception as e:
#                 print(f"Exception on predict_faces {e}")
#
#     #Function to handle button click
#     def start_camera(self, camera):
#         # self.frame_processed_callback = frame_processed_callback
#         encoder =trainer_main()
#         model = tf.keras.models.load_model('face_recognition_model.keras')
#         if model is None:
#             return
#         #Run face detection in a different Thread to avoid freezing
#
#         #Ambos procesos corren en simultaneo en distintos threads
#         detection = threading.Thread(target=self.detect_all_faces, args=(camera, ))
#         detection.daemon = True
#
#         prediction=threading.Thread(target=self.predict_faces, args=(model, ))
#         prediction.daemon = True
#
#         detection.start()
#         time.sleep(1) # Para evitar el problema de queue vacia desde un inicio. Darle un momento para q la camara cargue bien
#         prediction.start()
#
#         # detection.join()
#         # prediction.join()
#
#
#
#
