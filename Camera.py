import cv2 as cv # OpenCV 

class Camera(object):
    def __init__(self, broker):
        self.cap = cv.VideoCapture(0) # video capture source camera (Here webcam of lap>

        sending_video_stream = False


    # aqui se importan los métodos de la clase "Camera", que están organizados en ficheros.
    # Así podría orgenizarse la aportación de futuros alumnos que necesitasen incorporar nuevos servicios
    # para sus aplicaciones. Crearían un fichero con sus nuevos métodos y lo importarían aquí

    from functions.take_picture_func import take_picture
    from functions.video_stream_func import send_video_stream, start_video_stream, stop_video_stream
