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
version = "1.0.0"

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
        print("Confidence: ", confidence, "%")

        if confidence > 60.000:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom), (150, 150, 0), 2)
                cv2.putText(frame, name, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
            liveRecognition.stasis("rf", 0)
            global detected
            detected += 1
        else:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)
            liveRecognition.stasis("f", 0)



    def stasis(state, t):
        print("===", state, "===")
        if state == "rf":
            print("Face recognised, continuing")

        elif state == "f":
            print("Face detected, still continuing")

        elif state == "nrf":
            t2 = time.perf_counter()
            print("No face detected, beginning stasis")
            elapsed = t - t2
            print("{} seconds since last face detected".format(round(elapsed, 4)))
            liveRecognition.recogStart(1)
            
        

    def load(frame, mod, t):
        print("Encoding frame")
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=mod)
        face = face_recognition.face_encodings(rgb, boxes)
        print("=== FACE ===: ", face)
        print("FACE ARR LENGTH: ", len(face))
       
        t1 = time.perf_counter()
        print(f"Execution time {t1 - t:0.4f}s")
        global failed

        if failed > 30:
            print("=== Suspending ===")
            global totalSuspension
            totalSuspension += 1
            time.sleep(60)
            failed = 1
            print("=== Resuming ===")

        if face == []:
            print("No. of frames with no face: ", failed)
            failed += 1
            liveRecognition.recogStart(1) 
        else: 
            failed = 1
            liveRecognition.recognise(pickledData, face[0], boxes, frame)
       


    def recogStart(a):
        while True:
            print("\nCONFIRMED FACES = ", detected)
            print("FAILED FACES = ", failed)

            if detected > 5:
                return True
                break
            
            if totalSuspension > 1:
                return False
                break
            
            frame = video.read()
            if a == 0:
                frame = imutils.resize(frame, width=1020)
                liveRecognition.load(frame, model, 0)
                cv2.imshow("Video", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("k"):
                    break

            elif a == 1:
                t1 = time.perf_counter()
                frame = imutils.resize(frame, width=1020)
                liveRecognition.load(frame, model, t1)
                cv2.imshow("Video", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("k"):
                    break


    def main(self):
        global failed
        failed = 1

        global detected
        detected = 0

        global totalSuspension
        totalSuspension = 0

        print("Starting video...")
        global video
        video = VideoStream().start()

        if video is None:
            raise IOError("CANNOT START VIDEO")

        time.sleep(1.0)
        result = liveRecognition.recogStart(0)

        if result == True:
            return True
        elif result == False:
            return False

res = liveRecognition().main()
print(res)
