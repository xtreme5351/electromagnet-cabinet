import os
import sys
import cv2
import time
import pickle
import imutils
import argparse
from os import path
import face_recognition
from imutils import paths
from imutils.video import VideoStream
from imutils.video import FPS

pickledData = r"D:\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\faceEncoding.pkl"
model = "hog"

class liveRecognition():

    def recognise(orgEncoding, inpEncoding, boxes, frame):
        names = ["boi"]
        name = 'boi'
        print(type(orgEncoding))
        print(type(inpEncoding))
        data = pickle.loads(open(orgEncoding, "rb").read())
        print(type(data))

        print("[Beep boop] Comparing faces...")
        temp = []

        for i in range(len(data['encodings'])):
            print("=== Encoding no: ", i, " ===")
            temp.append(data['encodings'][i])

        print("RECOG =======")
        print(temp[1])
        results = face_recognition.compare_faces(temp, inpEncoding, tolerance=0.55)

        print(results)
        check = 0

        for x in results:
            if x == True:
                check += 1

        confidence = (check / len(temp)) * 100
        print("Positive Percentage: ", confidence, "%")

        if confidence > 60.000:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom), (150, 150, 0), 2)
                cv2.putText(frame, name, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
        else:
            pass



    def load(frame, mod):
        print("Encoding frame")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=mod)
        face = face_recognition.face_encodings(rgb, boxes)
        print("=== FACE ===: ", face)
        print("FACE ARR LENGTH: ", len(face))
        global returned
        if not face:
            liveRecognition.recogStart(1)
        else: 
            returned = face[0]

        liveRecognition.recognise(pickledData, returned, boxes, frame)
       


    def recogStart(a):
        while True:
            frame = video.read()
            if a == 0:
                frame = imutils.resize(frame, width=1020)
                liveRecognition.load(frame, model)
                cv2.imshow("Video", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("k"):
                    break

                time.sleep(2.0)
                # cv2.destroyWindow("Video")

            elif a == 1:
                liveRecognition.load(frame, model)
                cv2.imshow("Video", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("k"):
                    break

                time.sleep(2.0)



    def __init__(self):
        print("Starting video...")
        global video
        video = VideoStream().start()

        if video is None:
            raise IOError("CANNOT START VIDEO")

        time.sleep(1.0)
        liveRecognition.recogStart(0)

liveRecognition()
