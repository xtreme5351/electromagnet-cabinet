#!/user/bin/env python
# This is meant to run on a raspberry pi

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import twilio
from twilio.rest import Client
import time
import sys

#facial recognition import from the same directory
from .recognition import imageRecognition as ai

reader = SimpleMFRC522()
# This was to setup the Twilio client, but I never used it as ti was too expensive
# client = Client("Twilio Token 1", "Twilio Token 2")
# GPIO setup
relayPin = 11
GPIO.setup(relayPin, GPIO.OUT)
GPIO.setwarnings(False)
n = True
failedAttempts = []

# This function is called once 10 attempts have been exceeded, in order to restart the function again,
# the master card must be placed on the rfid, otherwise the script will kill itself (without clearing the GPIO)
# so the electromagnet still stays on. The killed script will have to manually restarted by a user.
def end():
    # Reads and outputs the ID (in integer values) and the text associated with the rfid
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


# Output to the console if the cabinet has been opened
def release():
    print("Opened")
    GPIO.output(relayPin, GPIO.LOW)
    
# Testing the electromagnet locking
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
        
        # Checks to see if the rfid tag is the same as the known tag of the master key.
        # If so, turns off the magnet for 30 secs
        if id == 758755130931:
            print("Master authorisation approved: SUCCESS")
            release()
            time.sleep(30)
            lock(0)
            
        # Checks to see if the rfid tag is the same as the known tag of the regular key.
        # If so, turns off the magnet for 10 secs
        elif id == 922657274647:
            print("Authorisation approved: SUCCESS")
            release()
            time.sleep(10)
            lock(2)
        # If the tag is unknown, it is unauthorised. 1 is appended to the list 'failedAttempts'
        # The length of the list determines the current attempts. 
        else:
            print("Unauthorised access: FAILED")
            failedAttempts.append(1)
            lock(1)
    else:
        # Calls the end function if the maximum number of failed attempts has reached 10
        print("Locked out of system. Place master key.")
        end()


# Infinite loop to run the code indefinitely, until it exits itself.
# Runs as long as the raspberry pi is on.
try:
    while n:
        main()

finally:
    pass

