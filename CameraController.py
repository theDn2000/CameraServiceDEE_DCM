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

local_broker_address = "localhost"
local_broker_port = 1883
sending_video_stream = False


def opencv_operations(hsv, lower_colour, upper_colour):
    mask = None
    mask = cv.inRange(hsv, lower_colour, upper_colour)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=5)
    mask = cv.dilate(mask, kernel, iterations=5)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    return cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


def direction_detector(img, send_commands, origin):
    global client
    global hsv_values

    # color must be detected in the whole picture
    area = "big"
    # color must be detected within the small rectangle
    # area = 'small'

    # Convert BGR to HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # clear LEDs
    client.publish(f"cameraService/{origin}/clear")

    # define range of colors in HSV
    lower_yellow = np.array([hsv_values[0], 50, 50])
    upper_yellow = np.array([hsv_values[1], 255, 255])

    lower_green = np.array([hsv_values[2], 50, 50])
    upper_green = np.array([hsv_values[3], 255, 255])

    lower_blue_s = np.array([hsv_values[4], 50, 50])
    upper_blue_s = np.array([hsv_values[5], 255, 255])

    lower_blue_l = np.array([hsv_values[6], 50, 50])
    upper_blue_l = np.array([hsv_values[7], 255, 255])

    lower_pink = np.array([hsv_values[8], 50, 50])
    upper_pink = np.array([hsv_values[9], 255, 255])

    lower_purple = np.array([hsv_values[10], 50, 50])
    upper_purple = np.array([hsv_values[11], 255, 255])

    detected_colour = "none"

    # ignore selected contour with area less that this
    minimum_size = 0

    area_biggest_contour = 0

    # for each color:
    #   find contours of this color
    #   get the biggest contour
    #   check if the contour is within the target rectangle (if area = 'small')
    #   check if the contour has the minimun area
    #   keet this contour if it is the biggest by the moment
    contours, hierarchy = opencv_operations(hsv, lower_yellow, upper_yellow)
    if len(contours) > 0:
        cyellow = max(contours, key=cv.contourArea)
        m = cv.moments(cyellow)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        if area == "big" or (c_x in range(210, 420) and c_y in range(160, 320)):
            if cv.contourArea(cyellow) > area_biggest_contour:
                area_biggest_contour = cv.contourArea(cyellow)
                detected_colour = "yellow"

    contours, hierarchy = opencv_operations(hsv, lower_green, upper_green)
    if len(contours) > 0:
        c_green = max(contours, key=cv.contourArea)
        m = cv.moments(c_green)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        if area == "big" or (c_x in range(210, 420) and c_y in range(160, 320)):
            if cv.contourArea(c_green) > area_biggest_contour:
                area_biggest_contour = cv.contourArea(c_green)
                detected_colour = "green"

    contours, hierarchy = opencv_operations(hsv, lower_blue_s, upper_blue_s)
    if len(contours) > 0:
        c_blue_s = max(contours, key=cv.contourArea)
        m = cv.moments(c_blue_s)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        if area == "big" or (c_x in range(210, 420) and c_y in range(160, 320)):
            if cv.contourArea(c_blue_s) > area_biggest_contour:
                area_biggest_contour = cv.contourArea(c_blue_s)
                detected_colour = "blue strong"

    contours, hierarchy = opencv_operations(hsv, lower_blue_l, upper_blue_l)
    if len(contours) > 0:
        c_blue_l = max(contours, key=cv.contourArea)
        m = cv.moments(c_blue_l)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        if area == "big" or (c_x in range(210, 420) and c_y in range(160, 320)):
            if cv.contourArea(c_blue_l) > area_biggest_contour:
                area_biggest_contour = cv.contourArea(c_blue_l)
                detected_colour = "blue light"

    contours, hierarchy = opencv_operations(hsv, lower_pink, upper_pink)
    if len(contours) > 0:
        c_pink = max(contours, key=cv.contourArea)
        m = cv.moments(c_pink)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        if area == "big" or (c_x in range(210, 420) and c_y in range(160, 320)):
            if cv.contourArea(c_pink) > area_biggest_contour:
                area_biggest_contour = cv.contourArea(c_pink)
                detected_colour = "pink"

    contours, hierarchy = opencv_operations(hsv, lower_purple, upper_purple)
    if len(contours) > 0:
        c_purple = max(contours, key=cv.contourArea)
        m = cv.moments(c_purple)
        c_x = int(m["m10"] / m["m00"])
        c_y = int(m["m01"] / m["m00"])
        if area == "big" or (c_x in range(210, 420) and c_y in range(160, 320)):
            if cv.contourArea(c_purple) > area_biggest_contour:
                area_biggest_contour = cv.contourArea(c_purple)
                detected_colour = "purple"

    if detected_colour != "none" and area_biggest_contour > minimum_size:
        cv.putText(
            img=img,
            text=detected_colour,
            org=(50, 50),
            fontFace=cv.FONT_HERSHEY_TRIPLEX,
            fontScale=1,
            color=(0, 0, 0),
            thickness=1,
        )
        # show color in LEDs
        command = detected_colour + "i"
        client.publish(f"cameraService/{origin}/{command}")
        # send command to autopilot if required
        if send_commands:
            if detected_colour == "purple":
                client.publish(f"cameraService/{origin}/drop")
                client.publish(f"cameraService/{origin}/RTL")
            elif detected_colour == "blue strong":
                client.publish(f"cameraService/{origin}/go", "North")
            elif detected_colour == "yellow":
                client.publish(f"cameraService/{origin}/go", "East")
            elif detected_colour == "green":
                client.publish(f"cameraService/{origin}/go", "West")
            elif detected_colour == "pink":
                client.publish(f"cameraService/{origin}/go", "South")

    # include rectangle in frame if area = 'small'
    if area == "small":
        cv.rectangle(img, (210, 160), (420, 320), (0, 255, 0), 3)


def send_video_stream(commands, message) -> Any:
    global sending_video_stream
    cap = cv.VideoCapture(0)
    splitted = message.split("/")
    origin = splitted[0]

    while sending_video_stream:
        # Read Frame
        topic_to_publish = f"cameraService/{origin}/videoFrame"
        ret, frame = cap.read()
        if "circus" in origin.lower():
            if ret:
                # detect direction and insert annotation in frame
                direction_detector(frame, commands, origin)
                _, image_buffer = cv.imencode(".jpg", frame)
                jpg_as_text = base64.b64encode(image_buffer)
                client.publish(topic_to_publish, jpg_as_text)
                time.sleep(0.1)
        # Encoding the Frame
        else:
            _, image_buffer = cv.imencode(".jpg", frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(image_buffer)
            # Publishing the Frame on the Topic home/server
            client.publish(topic_to_publish, jpg_as_text)
            time.sleep(0.1)
    cap.release()


def send_video_for_calibration(message):
    global sending_video_for_calibration
    cap = cv.VideoCapture(0)
    splitted = message.split("/")
    origin = splitted[0]

    while sending_video_for_calibration:
        # Read Frame
        ret, frame = cap.read()
        if ret:

            cv.circle(frame, (106, 120), 50, (0, 255, 255), 3)
            cv.putText(
                img=frame,
                text="Yellow here",
                org=(106, 120),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.5,
                color=(0, 255, 255),
                thickness=1,
            )

            cv.circle(frame, (319, 120), 50, (0, 255, 0), 3)
            cv.putText(
                img=frame,
                text="Green here",
                org=(319, 120),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=1,
            )

            cv.circle(frame, (532, 120), 50, (240, 106, 23), 3)
            cv.putText(
                img=frame,
                text="Blue Strong here",
                org=(532, 120),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.5,
                color=(240, 106, 23),
                thickness=1,
            )

            cv.circle(frame, (106, 360), 50, (250, 240, 30), 3)
            cv.putText(
                img=frame,
                text="Blue Light here",
                org=(106, 360),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.5,
                color=(250, 240, 30),
                thickness=1,
            )

            cv.circle(frame, (319, 360), 50, (139, 1, 240), 3)
            cv.putText(
                img=frame,
                text="Pink here",
                org=(319, 360),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.5,
                color=(139, 1, 240),
                thickness=1,
            )

            cv.circle(frame, (532, 360), 50, (240, 29, 140), 3)
            cv.putText(
                img=frame,
                text="Purple here",
                org=(532, 360),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.5,
                color=(240, 29, 140),
                thickness=1,
            )

            _, image_buffer = cv.imencode(".jpg", frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(image_buffer)
            client.publish(f"cameraService/{origin}/videoForCalibration", jpg_as_text)
        time.sleep(0.25)


def calibrate(frame, message):
    global hsv_values
    splitted = message.topic.split("/")
    origin = splitted[0]

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # for each color (circle) generate 50 random points
    # and keep the max and min H values
    # cabibrate yellow
    yellow_circle = Circle((106, 120), radius=50)
    yellow_max = -1
    yellow_min = 300
    for n in range(1, 50):
        x = random.randint(50, 150)
        y = random.randint(70, 170)
        if yellow_circle.contains_point([x, y]):
            value = hsv[y, x][0]
            if value > yellow_max:
                yellow_max = value
            if value < yellow_min:
                yellow_min = value

    # cabibrate green
    green_circle = Circle((319, 120), radius=50)
    green_max = -1
    green_min = 300
    for n in range(1, 50):
        x = random.randint(270, 370)
        y = random.randint(70, 170)
        if green_circle.contains_point([x, y]):
            value = hsv[y, x][0]
            if value > green_max:
                green_max = value
            if value < green_min:
                green_min = value

    # cabibrate blue strong
    blue_s_circle = Circle((532, 120), radius=50)
    blue_s_max = -1
    blue_s_min = 300
    for n in range(1, 50):
        x = random.randint(480, 580)
        y = random.randint(70, 170)
        if blue_s_circle.contains_point([x, y]):
            value = hsv[y, x][0]
            if value > blue_s_max:
                blue_s_max = value
            if value < blue_s_min:
                blue_s_min = value

    # cabibrate blue light
    blue_l_circle = Circle((106, 360), radius=50)
    blue_l_max = -1
    blue_l_min = 300
    for n in range(1, 50):
        x = random.randint(56, 156)
        y = random.randint(300, 400)
        if blue_l_circle.contains_point([x, y]):
            value = hsv[y, x][0]
            if value > blue_l_max:
                blue_l_max = value
            if value < blue_l_min:
                blue_l_min = value

    # cabibrate pink
    pink_circle = Circle((319, 360), radius=50)
    pink_max = -1
    pink_min = 300
    for n in range(1, 50):
        x = random.randint(270, 360)
        y = random.randint(310, 410)
        if pink_circle.contains_point([x, y]):
            value = hsv[y, x][0]
            if value > pink_max:
                pink_max = value
            if value < pink_min:
                pink_min = value
    # cabibrate purple
    purple_circle = Circle((532, 360), radius=50)
    purple_max = -1
    purple_min = 300
    for n in range(1, 50):
        x = random.randint(480, 580)
        y = random.randint(310, 410)
        if purple_circle.contains_point([x, y]):
            value = hsv[y, x][0]
            if value > purple_max:
                purple_max = value
            if value < purple_min:
                purple_min = value

    # include a margin of 2 units for min and max values
    margin = 2
    hsv_values = [
        int(yellow_min) - margin,
        int(yellow_max) + margin,
        int(green_min) - margin,
        int(green_max) + margin,
        int(blue_s_min) - margin,
        int(blue_s_max) + margin,
        int(blue_l_min) - margin,
        int(blue_l_max) + margin,
        int(pink_min) - margin,
        int(pink_max) + margin,
        int(purple_min) - margin,
        int(purple_max) + margin,
    ]
    values_json = json.dumps(hsv_values)
    client.publish(f"cameraService/{origin}/calibrationResult", values_json)


def on_message(client, userdata, message) -> Any:
    global sending_video_stream
    global taking_pictures
    global GWYB
    global sending_video_stream
    global sending_video_for_calibration
    global cap
    global hsv_values

    splitted = message.topic.split("/")
    origin = splitted[0]
    command = splitted[2]

    if command == "connectPlatform":
        print("Camera service connected by " + origin)

        # aqui en realidad solo debería subscribirse a los comandos que llegan desde el dispositivo
        # que ordenó la conexión, pero esa información no la tiene porque el origen de este mensaje
        # es el gate. NO COSTARIA MUCHO RESOLVER ESTO. HAY QUE VER SI ES NECESARIO

        client.subscribe("+/cameraService/#")

    if command == "takePicture":
        print("Take picture")
        cap = cv.VideoCapture(0)  # video capture source camera (Here webcam of laptop)
        for n in range(10):
            # this loop is required to discard first frames
            ret, frame = cap.read()
            _, image_buffer = cv.imencode(".jpg", frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(image_buffer)
            client.publish("cameraService/" + origin + "/picture", jpg_as_text)
        cap.release()

    if command == "startVideoStream":
        sending_video_stream = True
        w = threading.Thread(
            target=send_video_stream,
            args=(
                True,
                message.topic,
            ),
        )
        w.start()

    if command == "stopVideoStream":
        sending_video_stream = False

    if command == "set_hsv_values":
        # new values are received
        hsv_values = json.loads(message.payload)

    if command == "startGuideWithColors":
        sending_video_stream = True
        # Send video stream with direction annotation
        # AND SEND commands to autopilot
        w = threading.Thread(
            target=send_video_stream,
            args=(
                True,
                message.topic,
            ),
        )
        w.start()

    if command == "showVideoStream":
        sending_video_stream = True
        # Send video stream with direction annotation
        # BUT DO NOT send commands to autopilot
        w = threading.Thread(
            target=send_video_stream,
            args=(
                False,
                message.topic,
            ),
        )
        w.start()

    if command == "calibrate":
        sending_video_for_calibration = False
        # take the picture to be used for calibration
        ret, frame = cap.read()
        w = threading.Thread(
            target=calibrate,
            args=(
                frame,
                message.topic,
            ),
        )
        w.start()

    if command == "startVideoForCalibration":
        sending_video_for_calibration = True
        w = threading.Thread(target=send_video_for_calibration, args=(message.topic,))
        w.start()

    if command == "stopVideoForCalibration":
        sending_video_for_calibration = False

    if command == "getCurrentValues":
        print("Send current values", hsv_values)
        hsv_values_json = json.dumps(hsv_values)
        client.publish(f"cameraService/{origin}/currentValues", hsv_values_json)


hsv_values = [25, 38, 152, 170, 50, 60, 90, 110, 168, 175, 45, 67]
GWYB = False
client = mqtt.Client("Camera service")
client.on_message = on_message
client.connect(local_broker_address, local_broker_port)
client.loop_start()
print("Waiting connection from DASH...")
client.subscribe("gate/cameraService/connectPlatform")
