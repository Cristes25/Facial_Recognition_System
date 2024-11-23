from cProfile import label

import cv2
import numpy as np
from database_connection import Connector
import json
#New imports
from PIL import Image
import io
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

connection = Connector()


#get student picture and id from db
def get_training_data():
    global connection
    cursor = connection.mycursor
    query = "SELECT * FROM student_image_info"
    connection.mycursor.execute(query)
    data = cursor.fetchall()
    faces = []
    labels = []

    for row in data:
        # Check the correct id is being called here
        student_name = row[1] #mandar a llamar el id tmb para mandar eso, al parecer no acepta el string
        picture_blob = row[0]

        #Convert data to image
        np_image = np.frombuffer(picture_blob, dtype=np.uint8)
        face_image = cv2.imdecode(np_image, cv2.IMREAD_GRAYSCALE)
        # Turn all images into the same size, needed to create the model
        resized_image = cv2.resize(face_image, (224, 224)) #Keep the size small, por el bien de la computadora

        if face_image is not None:
            faces.append(resized_image)
            labels.append(student_name)

    #The model uses numbers, so its necessary to encode the labels. There is a function label_encoder.inverse_transform that
    # decodes into the string again, to use the name
    label_encoder = LabelEncoder()
    numeric_labels = label_encoder.fit_transform(labels)
    dataset = tf.data.Dataset.from_tensor_slices((faces, numeric_labels))
    return  dataset, numeric_labels

def create_model(dataset, input_shape=(224,224, 1)): # Third number represents channels, greyscale images use 1 channel, RGB use 3, to keep in mind if we wnat to change to color
    # Combine all labels into a single tensor
    # Method 1
    # all_labels = tf.concat([_ for x, _ in dataset], axis=0)
    # unique_labels = tf.unique(all_labels)

    # Method 2
    labels = dataset.map(lambda x, y: y) # Get the labels as np object
    unique_labels = labels.apply(tf.data.experimental.unique())
    unique_labels_list = list(unique_labels.as_numpy_iterator()) #Turn them into a list

    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),  # Embedding layer
        layers.Dense(len(set(unique_labels_list)), activation='softmax')  # Output layer with softmax for classification
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def train_face_recognizer():
    #Get the dataset
    dataset = get_training_data()
    # Call model to train
    model = create_model(dataset)
    return model
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # face_recognizer.train(faces, np.array(numeric_labels))
    #
    # #Extracting trained model data to Save into JSon  file
    # #LBPHF Methods
    # recognizer_data = {
    #     "labels": labels,
    #     "radius": face_recognizer.getRadius(),
    #     "neighbors": face_recognizer.getNeighbors(),
    #     "grid_x": face_recognizer.getGridX(),
    #     "grid_y": face_recognizer.getGridY(),
    #     "threshold": face_recognizer.getThreshold()
    # }
    # #Save the data to a JSON file
    # with open("trained_model.json", "w") as json_file:
    #     json.dump(recognizer_data, json_file)
    # return face_recognizer, label_map


def trainer_main():
    #connection=get_db_connection()
    if connection is None:
        print("Database connection failed. Exiting...")
        return

    print("Fetching training data...")
    dataset, labels = get_training_data()
    # if not faces:
    #     print("No training data found. Exiting...")
    #     connection.close()
    #     return
    #
    # print(f"Training with {len(faces)} images...")
    model = create_model(dataset)

    print("Training complete!")
    return model, labels
