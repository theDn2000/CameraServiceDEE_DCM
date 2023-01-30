
from typing import Any

import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import base64
import threading
import time
import random
import json
from matplotlib.patches import Circle


def send_video_stream( origin, client):
    global sending_video_stream
    global cap
    topic_to_publish = f"cameraService/{origin}/videoFrame"


    while sending_video_stream:
        # Read Frame
        ret, frame = cap.read()
        if ret:
            _, image_buffer = cv.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(image_buffer)
            client.publish(topic_to_publish, jpg_as_text)
            time.sleep(0.2)



def process_message(message, client):

    global sending_video_stream
    global cap




    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    print ('recibo ', command)

    if command == "takePicture":
        print("Take picture")
        ret = False
        for n in range (1,20):
            # this loop is required to discard first frames
            ret, frame = cap.read()
        _, image_buffer = cv.imencode(".jpg", frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(image_buffer)
        client.publish("cameraService/" + origin + "/picture", jpg_as_text)


    if command == "startVideoStream":
        print ('start video stream')
        sending_video_stream = True
        w = threading.Thread(
            target=send_video_stream,
            args=(
                origin,
                client
            ),
        )
        w.start()

    if command == "stopVideoStream":
        print ('stop video stream')
        sending_video_stream = False


def on_internal_message(client, userdata, message):
    print ('recibo internal ', message.topic)
    global internal_client
    process_message(message, internal_client)

def on_external_message(client, userdata, message):
    print ('recibo external ', message.topic)

    global external_client
    process_message(message, external_client)

def CameraService (connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state
    global cap

  sending_video_stream = False

    cap = cv.VideoCapture(0)  # video capture source camera (Here webcam of lap>


    print ('Camera ready')

    print ('Connection mode: ', connection_mode)
    print ('Operation mode: ', operation_mode)
    op_mode = operation_mode

    # The internal broker is always (global or local mode) at localhost:1884
    internal_broker_address = "localhost"
    internal_broker_port = 1884

    if connection_mode == 'global' and operation_mode == 'simulation':
        external_broker_address = external_broker
    if connection_mode == 'global' and operation_mode == 'production':
        external_broker_address = 'broker.hivemq.com'
    if connection_mode == 'local':
        external_broker_address = 'localhost'

    print ('External broker: ', external_broker_address)



    # the external broker must run always in port 8000
    external_broker_port = 8000



    external_client = mqtt.Client("Camera_external", transport="websockets")
    if external_broker_address == 'classpip.upc.edu':
        external_client.username_pw_set(username, password)

    external_client.on_message = on_external_message
    external_client.connect(external_broker_address, external_broker_port)


    internal_client = mqtt.Client("Camera_internal")
    internal_client.on_message = on_internal_message
    internal_client.connect(internal_broker_address, internal_broker_port)

    print("Waiting....")
    external_client.subscribe("+/cameraService/#", 2)
    internal_client.subscribe("+/cameraService/#")
    internal_client.loop_start()
    external_client.loop_forever()


if __name__ == '__main__':
    import sys
    connection_mode = sys.argv[1] # global or local
    operation_mode = sys.argv[2] # simulation or production
    username = None
    password = None
    if connection_mode == 'global' and operation_mode == 'simulation':
        external_broker = sys.argv[3]
        if external_broker == 'classpip.upc.edu':
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None

    CameraService(connection_mode,operation_mode, external_broker, username, password)


