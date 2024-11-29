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

from charset_normalizer import detect

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
        # self.face_queue = Queue(maxsize=30)
        self.last_frame = None
        self.detected_faces = []
        self.model = tf.keras.models.load_model('face_recognition_model.keras')


    def stop_and_capture(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.running = False
        if self.last_frame is not None:
            last_frame = self.qimage_to_np_array(self.last_frame)
            faces = self.predict_faces()
            return last_frame, faces  # Return the last frame
        return None

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

    def qimage_to_np_array(self, qimage):
        """Convert QImage to a NumPy array compatible with OpenCV."""
        qimage = qimage.convertToFormat(QImage.Format_RGB888)  # Ensure consistent format
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        arr = np.array(ptr).reshape((height, width, 3))
        return arr

    def hash_face(self, face_image):
        '''Create a unique hash for each face image based on its content.'''
        image_hash = hashlib.md5(face_image.tobytes()).hexdigest()
        return image_hash

    def detect_all_faces_in_livemode(self, cap):
        '''Detect faces in the video stream and add them to the queue.'''
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if face_cascade.empty():
                print("Error: Failed to load Haar Cascade Classifier.")
                return

            while self.running:
                ret, frame = self.cap.read()
                if ret or frame is None:  # Check if frame is valid
                    print("Warning: Failed to capture frame. Retrying...")
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
                self.last_frame = qt_image
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

    def detect_all_faces(self):
        while self.running:
            try:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                ret, frame = self.cap.read()
                if face_cascade.empty():
                    print("Error: Failed to load Haar Cascade Classifier.")
                    return
                # frame = self.qimage_to_np_array(frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(150, 50), maxSize=(350, 350))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    face = gray[y:y + h, x:x + w]
                    # Normalize and resize face for the model
                    face_resized = cv2.resize(face, (240, 240))
                    face_normalized = face_resized / 255.0
                    face_input = np.expand_dims(face_normalized, axis=0)
                    face_input = np.expand_dims(face_input, axis=-1)
                    self.detected_faces.append(face_input)
                qt_image = self.convert_to_frame(frame)
                self.last_frame = qt_image
                self.frame_processed_callback(qt_image)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    self.cap.release()
                    cv2.destroyAllWindows()

            except cv2.error as e:
                print("Error", f"OpenCV error: {e}")


    def predict_faces(self):
        present_students = []
        for face in self.detected_faces:
            prediction = self.model.predict(face)
            predicted_label = str(np.argmax(prediction))
            present_students.append(predicted_label)
        return present_students


    def predict_faces_in_livemode(self, model):
        '''Process the faces in the queue and make predictions.
        Uncomment self.queue, for now this is useless, since all it is doing is detecting faces in a photo,
        this is more for real time detection'''
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
        self.cap = camera
        if self.model is None:
            return
        # Run face detection and prediction in separate threads
        detection = threading.Thread(target=self.detect_all_faces, args=())
        detection.daemon = True

        # prediction = threading.Thread(target=self.predict_faces, args=(model,))
        # prediction.daemon = True

        detection.start()
        time.sleep(1)  # Give some time for camera to initialize
        # prediction.start()
        #
        # detection.join()
        # prediction.join()
