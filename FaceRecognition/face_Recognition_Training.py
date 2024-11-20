import cv2
import numpy as np
from database_connection import Connector
import json

connection = Connector()
#get student picture and id from db
def get_training_data():
    global connection
    cursor=connection.mycursor
    query= "SELECT * FROM student_images"
    connection.mycursor.execute(query)
    data=cursor.fetchall()
    faces=[]
    labels=[]

    for row in data:
        # Check the correct id is being called here
        student_id=row[1]
        picture_blob=row[3]

        #Convert data to image
        np_image=np.frombuffer(picture_blob, dtype=np.uint8)
        face_image=cv2.imdecode(np_image, cv2.IMREAD_GRAYSCALE)

        if face_image is not None:
            faces.append(face_image)
            labels.append(student_id)

    return faces, labels

def train_face_recognizer(faces, labels):
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))

    #Extracting trained model data to Save into JSon  file
    #LBPHF Methods
    recognizer_data={
        "labels": labels,
        "radius":face_recognizer.getRadius(),
        "neighbors":face_recognizer.getNeighbors(),
        "grid_x":face_recognizer.getGridX(),
        "grid_y":face_recognizer.getGridY(),
        "threshold":face_recognizer.getThreshold()
    }
    #Save the data to a JSON file
    with open("trained_model.json", "w") as json_file:
        json.dump(recognizer_data, json_file)
    print("Model Trained and saved as 'trained_model'")
    return face_recognizer

def trainer_main():
    #connection=get_db_connection()
    if connection is None:
        print("Database connection failed. Exiting...")
        return

    print("Fetching training data...")
    faces, labels = get_training_data()
    if not faces:
        print("No training data found. Exiting...")
        connection.close()
        return

    print(f"Training with {len(faces)} images...")
    recognizer = train_face_recognizer(faces, labels)

    print("Training complete!")
    return recognizer


