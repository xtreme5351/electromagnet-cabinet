#!/user/bin/env python
# This is meant to run on a raspberry pi

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import twilio
from twilio.rest import Client
import time
import sys

#ml import
from .recognition import imageRecognition as ai

reader = SimpleMFRC522()
# client = Client("ACbb9d715fd00b4684505a46100101556f", "1e55a26b888b1775d83775314a9f93c5")
relayPin = 11
GPIO.setup(relayPin, GPIO.OUT)
GPIO.setwarnings(False)
n = True
failedAttempts = []

def end():
    id, text = reader.read()
    print("ID: " + str(id))
    print("Text: " + str(text))
    if id == 758755130931:
        print("Master Authorisation approved: SUCCESS")
        failedAttempts.clear()
        main()
    else:
        print("Sorry locked out. Restart script.")
        sys.exit()



def release():
    print("Opened")
    GPIO.output(relayPin, GPIO.LOW)

def lock(x):
    if x == 0:
        print("Locked")
    if x == 1:
        print("D:")
    else:
        print(":D")
    GPIO.output(relayPin, GPIO.HIGH)


def main():
    if len(failedAttempts) < 10:
        print("=== Starting ===")
        print("Failed attempts = ",len(failedAttempts))
        GPIO.output(relayPin, GPIO.HIGH)
        id, text = reader.read()
        print("ID: " + str(id))
        print("Text: " + str(text))
        if id == 758755130931:
            print("Master authorisation approved: SUCCESS")
            release()
            time.sleep(30)
            lock(0)
        elif id == 922657274647:
            print("Authorisation approved: SUCCESS")
            release()
            time.sleep(10)
            lock(2)
        else:
            print("Unauthorised access: FAILED")
            failedAttempts.append(1)
            lock(1)
    else:
        print("Locked out of system. Place master key.")
        end()



try:
    while n:
        main()

finally:
    pass

