#!../.venv/bin/python
from belt import Belt
from server import Server
from camera import Camera
import logging
import signal
import sys

# Configure logs to log both in the console and to a file
logger = logging.getLogger(__name__)
logging.basicConfig(handlers=[logging.FileHandler("logs/latest.log"),
                              logging.StreamHandler(sys.stdout)],
                    encoding='utf-8', level=logging.DEBUG)

# Gracefully stop the server when the program exits or crashes
# This makes sure to stop the cameras and later unpower the steppers


def sigterm_handler(_signo, _stack_frame):
    logger.info("stopping server...")
    Server.stop()
    # TODO: stop stepper motors
    sys.exit(0)


if __name__ == "__main__":
    # Register our shutdown handler to be called at signal "terminate"
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Start the server and add the camera(s)
    logger.info("starting")
    camera = Camera()
    Server.addCamera(camera)
    try:
        Server.start()
    finally:
        sigterm_handler(signal.SIGTERM, 0)
