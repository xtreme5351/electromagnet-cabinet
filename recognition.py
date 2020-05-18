import cv2
import pickle
import argparse
import face_recognition
from imutils import paths
from imutils.video import VideoStream
import os
from os import path
import time

# testDataset = r"D:\Pranav\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputEncoding.pkl"
testImage1 = r"D:\Pranav\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputs\0000.png"
testImage2 = r"D:\Pranav\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputs\0002.jpeg"
testImage3 = r"D:\Pranav\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputs\0003.jpeg"
orgFile = r"D:\Pranav\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\verified\0001.png"
pickledData = r"D:\Pranav\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\faceEncoding.pkl"
model = "cnn"

class imageRecognition():
    def loadImgs(self, dir, mod):

        print("Encoding image at path: ", dir)

        image = cv2.imread(dir)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=mod)
        face = face_recognition.face_encodings(rgb, boxes)

        # print("Returning encoding: ",face[0])
        return face[0], boxes, image
   
  
    def recogniseFaces(self, orgEncoding, inpEncoding, boxes, photo):
        names = ["pranav"]
        name = 'pranav'
        print(type(orgEncoding))
        print(type(inpEncoding))
        data = pickle.loads(open(orgEncoding, "rb").read())
        print(type(data))

        print("[Beep boop] Comparing faces...")
        temp = []

        for i in range(len(data['encodings'])):
            print("=== Encoding no: ", i, " ===")
            # print(data['encodings'][i])
            temp.append(data['encodings'][i])

        print("=======")
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
                cv2.rectangle(photo, (left, top), (right, bottom), (150, 150, 0), 2)
                cv2.putText(photo, name, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
                    
        cv2.imshow("Screen", photo)
        cv2.waitKey(ord("k"))
        time.sleep(20)



    def __init__(self):
        #ag = argparse.ArgumentParser()
        #ag.add_argument("-s", "--dataset", required=True,
        #                help="dataset dir")
        #ag.add_argument("-d", "--model", type=str, default="cnn",
        #                help="CNN or hog")
        #ag.add_argument("-i", "--input", type=str, required=True,
        #                help="input image")
        #args = vars(ag.parse_args())
        print("Starting ...")
        # org = self.loadImgs(orgFile, model)
        print("Photo comparision 1")
        comp1, box1, img = self.loadImgs(testImage2, model)
        self.recogniseFaces(pickledData, comp1, box1, img)


imageRecognition()
