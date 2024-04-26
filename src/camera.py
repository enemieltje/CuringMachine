from threading import Condition
import io
import time
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class Camera:
    picam2: Picamera2
    videoConfig: dict
    captureConfig: dict

    def __init__(self) -> None:

        # Create Picamera2 instance and configure it
        self.picam2 = Picamera2()
        self.configure()

    def configure(self):
        self.videoConfig = self.picam2.create_video_configuration(
            main={"size": (640, 480)})
        self.captureConfig = self.picam2.create_still_configuration()

        self.picam2.configure(self.videoConfig)

    def startStream(self):
        print("start stream")
        self.picam2.start_recording(JpegEncoder(), FileOutput(output))

    def stopStream(self):
        print("stop stream")
        self.picam2.stop_recording()

    def picture(self, path=(str(time.asctime()) + ".jpeg")):
        self.picam2.switch_mode_and_capture_file(
            self.captureConfig, path, "main", delay=10)

        with open(path, 'rb') as file_handle:
            return file_handle.read()
        # return path


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


output = StreamingOutput()
