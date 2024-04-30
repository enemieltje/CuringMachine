#!../.venv/bin/python
from curingMachine import CuringMachine
import logging
import signal
import sys

# Configure logs to log both in the console and to a file
logger = logging.getLogger(__name__)
logging.basicConfig(handlers=[logging.FileHandler("logs/latest.log"),
                              logging.StreamHandler(sys.stdout)],
                    encoding='utf-8', level=logging.DEBUG)

# Gracefully stop the server when the program exits or crashes
# This makes sure to stop the cameras and unpower the steppers


def sigterm_handler(_signo, _stack_frame):
    logger.info("stopping server...")
    CuringMachine.stop()
    sys.exit(0)


if __name__ == "__main__":
    # Register our shutdown handler to be called at signal "terminate"
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Start the server and add the camera(s)
    logger.info("starting")
    try:
        CuringMachine.start()
    finally:
        sigterm_handler(signal.SIGTERM, 0)
