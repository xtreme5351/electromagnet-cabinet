import cv2
import pickle
import argparse
import face_recognition
from imutils import paths
from imutils.video import VideoStream
import os
from os import path
import time

# === NOTE ===
# This was just a test script for me to properly understand and test out how facial recognition works in python.
# This was just a step to the finished project.
# I stil included it because I thought it was cool :p
# === END NOTE ===

# paths to images to test accuracy and recognition
testImage1 = r"D:\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputs\0000.png"
testImage2 = r"D:\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputs\0002.jpeg"
testImage3 = r"D:\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\inputs\0003.jpeg"

# path to original comparision file
orgFile = r"D:\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\verified\0001.png"

# path to pickled data of multiple photo encodings, in one file
pickledData = r"D:\PycharmProjects\python\machineLearning\ElectromagnetCabinet\dataset\faceEncoding.pkl"

# machine learning, classification method
model = "cnn"

class imageRecognition():
    # loads the images and creates encodings given a directory and a model
    def loadImgs(self, dir, mod):

        print("Encoding image at path: ", dir)

        image = cv2.imread(dir)
        # This is important to flip the colour format around so that the models can read it better.
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Creates encoding via the face recognition module
        boxes = face_recognition.face_locations(rgb, model=mod)
        face = face_recognition.face_encodings(rgb, boxes)

        # print("Returning encoding: ",face[0])
        return face[0], boxes, image
   
  
    def recogniseFaces(self, orgEncoding, inpEncoding, boxes, photo):
        # Names of people to be recognised, since its only me, its just 1 name
        names = ["boi"]
        name = 'boi'
        print(type(orgEncoding))
        print(type(inpEncoding))
        
        # Opens the pickled file of encoding data
        data = pickle.loads(open(orgEncoding, "rb").read())
        print(type(data))

        print("[Beep boop] Comparing faces...")
        temp = []
        # Loops over all the encodings and appends the data to a temporary directory
        for i in range(len(data['encodings'])):
            print("=== Encoding no: ", i, " ===")
            # print(data['encodings'][i])
            temp.append(data['encodings'][i])
            
        # The temp directory's data is then compared with the input image. This returns a list of True or False for each image.
        # True if the face matches with a certain tolerance
        # False if the face doesnt match
        print("=======")
        print(temp[1])
        results = face_recognition.compare_faces(temp, inpEncoding, tolerance=0.55)

        print(results)
        check = 0
        
        # Just a small check for all True images, returns the number of positive matches
        for x in results:
            if x == True:
                check += 1
                
        # Simple confidence of all images in the dataset put together into 1 percentage to represent the number of positive matches
        confidence = (check / len(temp)) * 100
        print("Positive Percentage: ", confidence, "%")
        
        # Applies a box around the face if the confidence is above 60%, this is for security purposes.
        # This means that at least 60% of the cases have to be a positive match with the dataset
        if confidence > 60.000:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(photo, (left, top), (right, bottom), (150, 150, 0), 2)
                cv2.putText(photo, name, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
                
        # Shows the image with the box and waits for the exit key            
        cv2.imshow("Screen", photo)
        cv2.waitKey(ord("k"))
        time.sleep(20)



    def __init__(self):
        # Potential parsing of arguments to be done within the command line but I just hard coded the values as this is a test script.
        # If you do this, then a lot of the input variables would have to be changed to args["whatever input name"]
        #ag = argparse.ArgumentParser()
        #ag.add_argument("-s", "--dataset", required=True, help="dataset dir")
        #ag.add_argument("-d", "--model", type=str, default="cnn", help="name of the model")
        #ag.add_argument("-i", "--input", type=str, required=True, help="input image")
        #args = vars(ag.parse_args())
        
        print("Starting ...")
        print("Photo comparision 1")
        comp1, box1, img = self.loadImgs(testImage2, model)
        # Takes the values returned from the loadImgs function and places them into the recogniseFaces function
        self.recogniseFaces(pickledData, comp1, box1, img)

# Runs the class
imageRecognition()
