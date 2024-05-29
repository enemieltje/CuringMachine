#!../.venv/bin/python
import logging
import signal
import sys
from loadcell import Loadcell
from belt import Belt
from config import Config
from input import Input
from menu import LcdMenu
from server import Server
from curingMachine import CuringMachine

# Configure logs to log both in the console and to a file
logger = logging.getLogger(__name__)
logging.basicConfig(handlers=[logging.FileHandler("logs/latest.log"),
                              logging.StreamHandler(sys.stdout)],
                    encoding='utf-8', level=logging.DEBUG)


def sigterm_handler(_signo, _stack_frame):
    # Gracefully stop the server when the program exits or crashes
    # This makes sure to stop the cameras and unpower the steppers
    logger.info("stopping...")
    LcdMenu.stop()
    CuringMachine.stop()
    Server.stop()
    LcdMenu.turnOff()
    sys.exit(0)


if __name__ == "__main__":
    # Register our shutdown handler to be called at signal "terminate"
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Start the server and add the camera(s)
    logger.info("starting")
    try:
        Config.start()
        CuringMachine.start()
        Loadcell.start()
        Input.start()
        LcdMenu.start()
        Server.start()
    finally:
        # CuringMachine.stop()
        sigterm_handler(signal.SIGTERM, 0)
