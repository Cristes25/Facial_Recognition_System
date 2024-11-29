# todo add the things from the training here
# Todo data augmentation here
import cv2
import numpy as np
from numpy.random import normal
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from database_connection import Connector

connection = Connector()

def get_faces_from_db():
    global connection
    data = connection.get_faces_from_db()
    faces = []
    labels = []

    for row in data:
        student_name = row[0]
        picture_blob = row[1]

        # Convert data to image
        np_image = np.frombuffer(picture_blob, dtype=np.uint8)
        face_image = cv2.imdecode(np_image, cv2.IMREAD_GRAYSCALE)
        # The image of the face has a lot of whitespace, detection doesnt, so try to eliminate that from the image here4
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        face = face_cascade.detectMultiScale(face_image, 1.1, 4)
        for (x, y, w, h) in face:
            face_region = face_image[y:y + h, x:x + w]
            # Turn all images into the same size, needed to create the model
            face_resized = cv2.resize(face_region, (240, 240)) # Keep the size small, chose this number
            # because its about the same size as the square taht forms arounds the face for detection
            face_normalized = face_resized / 255.0
            face_input = np.expand_dims(face_normalized, axis=-1)  # Add channel dimension

            # cv2.imshow(student_name, face_resized)
            # cv2.waitKey(0)
            images_batch = aumentate_data(face_input)

        if face_image is not None:
            faces.extend(images_batch)
            labels.extend([student_name] * len(images_batch))

    faces_normalized = np.array(faces, dtype=np.float32)
    return faces_normalized, labels

def aumentate_data(face):
    aumentated_images = []
    face = np.expand_dims(face, axis=0)
    datagen = ImageDataGenerator(
        rotation_range=40,  # Randomly rotate images in the range 0-40 degrees
        width_shift_range=0.2,  # Randomly shift images horizontally
        height_shift_range=0.2,  # Randomly shift images vertically
        shear_range=0.2,  # Randomly apply shearing transformations
        zoom_range=0.2,  # Randomly zoom in on images
        horizontal_flip=True,  # Randomly flip images horizontally
        fill_mode='nearest'  # Fill in pixels with nearest pixel value
    )
    for i, batch in enumerate(datagen.flow(face, batch_size=1)):
        aumentated_images.append(batch[0]) # Extract the augmented image from the batch
        if i == 9:  # Stop after generating 10 augmented images
            break
        break
    normalized = np.array(aumentated_images, dtype=np.float32)

    return normalized
