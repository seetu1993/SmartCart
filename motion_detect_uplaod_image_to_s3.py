import P3picam
import picamera
from picamera import PiCamera
import time
from time import sleep
import datetime as dt
import sys
import subprocess
import os

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import datetime
import random
import json 
import time
from ctypes import *
arducam_vcm =CDLL('/home/pi/RaspberryPi/Motorized_Focus_Camera/python/lib/libarducam_vcm.so')

motionState = False
BUCKET = "s3://smartcartphoto/"
SRC_DIR = "/home/pi/images/"
DEST = BUCKET + "images/"
CURRENT_DATE = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
counter = 1

myMQTTClient = AWSIoTMQTTClient("raspi")
myMQTTClient.configureEndpoint("aicn214q8070z-ats.iot.us-east-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("AmazonXXXX-XXX-1.pem","e5e2XXXXXXXX.key","e5e2920ff1-ceXXXXXXXXXXcrt")

myMQTTClient.connect()
print("Client Connected")
filePathsInThisEvent = []
processes = []
lastEvent = datetime.time()
arducam_vcm.vcm_init()

while True:
    motionState = P3picam.motion()
    print(motionState)
    if motionState:
        filePath = '/home/pi/images/'+str(counter)+'.jpg'
        filePathsInThisEvent.append(DEST + str(counter)+'.jpg')
        with picamera.PiCamera() as camera:
            arducam_vcm.vcm_write(502)
            camera.annotate_text = CURRENT_DATE
            camera.capture(filePath)
            counter = counter +1 
            arducam_vcm.vcm_write(522)

        print("picture taken")
        CMD = "s3cmd put --acl-public %s %s" % (filePath, DEST)
        processes.append(subprocess.Popen(CMD, shell=True))
    else:
        if len(filePathsInThisEvent) != 0:
            timestamp = datetime.datetime.now()
            message = { "FilePaths": filePathsInThisEvent , "cart_number": "1234"}
            print(message)
            topic = "iot/motionDetected"
            msg = json.dumps(message) 
            myMQTTClient.publish(topic, msg, 1) 
        processes = []
        filePathsInThisEvent = []