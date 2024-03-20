import base64
import cv2 as cv  # OpenCV
import threading
import time



def send_video_stream(self, origin, client, callback): # Parecido a telemetry_info (hay que pasarle una función de callback)
    

    while self.sending_video_stream:
        # Read Frame
        ret, frame = self.cap.read()
        if ret:
            _, image_buffer = cv.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(image_buffer)
            callback(origin, jpg_as_text)


def start_video_stream(self, origin, client):
    print("start video stream")
    self.sending_video_stream = True
    w = threading.Thread(target=send_video_stream, args=(origin, client),)
    w.start()

def stop_video_stream(self):
    print("stop video stream")
    self.sending_video_stream = False
    