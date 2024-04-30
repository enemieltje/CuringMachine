from threading import Condition
import io
import time
import logging
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

logger = logging.getLogger(__name__)


class StreamingOutput(io.BufferedIOBase):
    # The streaming output functions as a frame buffer where frames get saved to and read from
    # This way, the camera is not dependant on a reader, and even has support for multiple readers

    # The buffered IO base is a default python class. This StreamingOutput is a wrapper that notifies all readers when a frame is written.
    # This allows the preview to be updated as soon as a new frame arrives.
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class Camera:
    picam2: Picamera2
    videoConfig: dict
    captureConfig: dict
    isStreaming: bool
    streamingOutput: StreamingOutput

    def __init__(self) -> None:
        # Create Picamera2 instance and configure it
        self.picam2 = Picamera2()
        self.configure()

        # Configure streaming output for streaming the preview
        self.streamingOutput = StreamingOutput()
        self.isStreaming = False

    def configure(self):
        # The configuration to be used for the web preview
        self.videoConfig = self.picam2.create_video_configuration(
            main={"size": (640, 480)})

        # The configuration to be used for taking a picture (default for now)
        self.captureConfig = self.picam2.create_still_configuration()

        # Start by using the video config
        self.picam2.configure(self.videoConfig)

    def startStream(self):
        logger.debug("start stream")
        self.isStreaming = True
        self.picam2.start_recording(
            JpegEncoder(), FileOutput(self.streamingOutput))

    def stopStream(self):
        logger.debug("stop stream")
        self.isStreaming = False
        self.picam2.stop_recording()

    def picture(self, path=(str(time.asctime()) + ".png")):
        # Take a picture and save it to a file. If no file was specified, it gets saved with the current time as name
        wasStreaming = self.isStreaming
        logger.debug("taking picture: " + path)

        # Pause stream if needed
        if wasStreaming:
            self.stopStream()

        # Take the picture
        self.picam2.switch_mode_and_capture_file(
            self.captureConfig, path, "main", delay=10)

        # Restart stream if needed
        if wasStreaming:
            self.startStream()

        # Return the picture as a Byte Stream so it can be sent to a webpage directly
        with open(path, 'rb') as file_handle:
            return file_handle.read()
