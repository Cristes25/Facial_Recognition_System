import cv2
import numpy as np
#from connection module import get db connection
import os

import json


#get student picture and id from db
def get_training_data(connection):
    cursor=connection.cursor()
   # query= "SELECT student_id, student_picture FROM students WHERE student_picture IS NOT NULL "
    cursor.execute(query)
    data=cursor.fetchall()

    faces=[]
    labels=[]

    for row in data:
        student_id=row[0]
        picture_blob=row[1]

        #Convert data to image
        np_image=np.frombuffer(picture_blob, dtype=np.uint8)
        face_image=cv2.imdecode(np_image, cv2.IMREAD_COLOR)

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
        "histograms":[face_recognizer.getHistogram(i) for i in range(len(labels))],
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

def main():
    #connection=get_db_connection()
    if connection is None:
        print("Database connection failed. Exiting...")
        return

    print("Fetching training data...")
    faces, labels = get_training_data(connection)
    if not faces:
        print("No training data found. Exiting...")
        connection.close()
        return

    print(f"Training with {len(faces)} images...")
    train_face_recognizer(faces, labels)

    connection.close()
    print("Training complete!")


if __name__ == "__main__":
    main()




