#!../.venv/bin/python
from belt import Belt
from server import Server
from camera import Camera
import logging
import signal
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/latest.log',
                    filemode='w',
                    encoding='utf-8', level=logging.DEBUG)


def sigterm_handler(_signo, _stack_frame):
    logger.info("stopping server...")
    Server.stop()
    sys.exit(0)


# Create an instance of the Client class, and save it in a variable called client
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    # signal.signal(signal.SIGKILL, sigterm_handler)

    logger.info("starting")
    camera = Camera()
    Server.addCamera(camera)
    try:
        Server.start()
    finally:
        sigterm_handler(signal.SIGTERM, 0)
