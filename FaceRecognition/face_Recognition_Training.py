from cProfile import label

import cv2
import numpy as np
import json
#New imports
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os
import pickle
from FaceRecognition.image_conversion import get_faces_from_db

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def get_training_data():
    faces_aumented, labels = get_faces_from_db()
    print(labels)
    #The model uses numbers, so its necessary to encode the labels. There is a function label_encoder.inverse_transform that
    # decodes into the string again, to use the name. Must be the same encoder, thats why this one is sent around functions so much
    label_encoder = LabelEncoder()
    numeric_labels = label_encoder.fit_transform(labels)
    numeric_labels = tf.keras.utils.to_categorical(numeric_labels, num_classes=len(label_encoder.classes_))
    save_encoder(label_encoder)

    return numeric_labels, faces_aumented

def save_encoder(label_encoder, file_name='label_encoder.pkl'):
    try:
        with open(file_name, 'wb') as f:
            pickle.dump(label_encoder, f)
        print(f"LabelEncoder saved to {file_name}")
    except Exception as e:
        print(f"Error saving LabelEncoder: {e}")

def load_encoder(file_name='label_encoder.pkl'):
    try:
        with open(file_name, 'rb') as f:
            label_encoder = pickle.load(f)
        print(f"LabelEncoder loaded from {file_name}")
        return label_encoder
    except Exception as e:
        print(f"Error loading LabelEncoder: {e}")
        return None

def create_model():
    label_encoder = load_encoder()
    model = Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(240, 240, 1)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.AdamW(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def trainer_main():
    print("Fetching training data...")
    numeric_labels, faces_normalized = get_training_data()

    model = create_model()
    history = model.fit(faces_normalized, numeric_labels)
    #TODO Not urgent. Save and compare, check accuracy
    # https://www.tensorflow.org/tutorials/keras/save_and_load
    model.save('face_recognition_model.keras')
    print("Training complete!")
