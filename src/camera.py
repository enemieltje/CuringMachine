from threading import Condition
import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class Camera:
    picam2: Picamera2

    def __init__(self) -> None:

        # Create Picamera2 instance and configure it
        self.picam2 = Picamera2()
        self.configure()

    def configure(self):
        self.picam2.configure(self.picam2.create_video_configuration(
            main={"size": (640, 480)}))

    def startStream(self):
        self.picam2.start_recording(JpegEncoder(), FileOutput(output))

    def stopStream(self):
        self.picam2.stop_recording()


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


output = StreamingOutput()
