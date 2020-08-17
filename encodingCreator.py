from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = ["Boi"]

imagePath = 'X:\\PycharmProjects\\python\machineLearning\\ElectromagnetCabinet\\dataset\\inputs'
pickleFilePath = 'X:\\PycharmProjects\\python\\machineLearning\\ElectromagnetCabinet\\dataset\\inputEncoding.pkl'

tempArr = []
facesArr = []

for img in os.walk(imagePath):
	tempArr.append(img)

for i in range(0, 1):
    dir = imagePath + '\\' + tempArr[0][2][i]
    facesArr.append(dir)

print(facesArr)

print("Starting encoding ...")
for x in range(0, 1):
    print("Starting encoding number: ", x)
    path = facesArr[x]
    image = cv2.imread(path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model='cnn')
    encodings = face_recognition.face_encodings(rgb, boxes)

    # loop over the encodings
    for encoding in encodings:
        knownEncodings.append(encoding)


    data = {"encodings": knownEncodings}
    f = open(pickleFilePath, "wb")
    f.write(pickle.dumps(data))
    f.close()
    print("Finished encoding number: ", x)
