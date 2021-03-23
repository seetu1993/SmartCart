import time
import json
import subprocess
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import numpy as np
from keras_preprocessing import image
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.backend import set_session
import operator
from  dynamoDb import put_user_cart
from s3Read import s3
from predict import predictfruit
from barc import detect_code


myMQTTClient = AWSIoTMQTTClient("backendserver")
myMQTTClient.configureEndpoint("aicn214q8070z-ats.iot.us-east-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./Amaz-XXXX-XXXXem.txt","./73fdaeXXXX-XXXem.key", "./73fdae38XXXX-XXXXe.pem.crt")

myMQTTClient.connect()
print("Client Connected")

def customCallback(client,userdata,message):
    print("callback came...")
    print(message.payload)
    x = json.loads(message.payload)
    outbountMessage = ""
    code = "-1"
    localPaths = []
    foundCode = False
    #try read barcode if not then go to fruit classification
    for path in x["FilePaths"]:
        image_path = s3(path)
        print(image_path)
        localPaths.append(image_path)
        code = detect_code(image_path)
        if code is not None:
            foundCode = True
            break
    
    if foundCode:
        put_user_cart(code, x["cart_number"], "PackagedItems")
        return
    
    maxFreq = {}
    model = None
    for image_path in localPaths:
        print(image_path)
        fruit,model = predictfruit(image_path, model)
        if fruit not in maxFreq:
            maxFreq[fruit] = 0
        maxFreq[fruit] += 1
        print(fruit)
    fruits = max(maxFreq.items(), key=operator.itemgetter(1))[0]
    put_user_cart(fruits, message.cart_number, "FruitsAndVegitables")
    return

    


myMQTTClient.subscribe("iot/motionDetected", 1, customCallback)
print('waiting for the callback. Click to conntinue...')
x = input()
myMQTTClient.unsubscribe("general/outbound")
print("Client unsubscribed")
myMQTTClient.disconnect()
print("Client Disconnected")

