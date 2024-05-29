#!../.venv/bin/python
import logging
import signal
import sys
from curingMachine import CuringMachine

# Configure logs to log both in the console and to a file
logger = logging.getLogger(__name__)
logging.basicConfig(handlers=[logging.FileHandler("logs/latest.log"),
                              logging.StreamHandler(sys.stdout)],
                    encoding='utf-8', level=logging.DEBUG)


if __name__ == "__main__":
    # Register our shutdown handler to be called at signal "terminate"
    signal.signal(signal.SIGTERM, CuringMachine.stop)

    # Start the server and add the camera(s)
    logger.info("starting")
    try:
        CuringMachine.start()
    finally:
        CuringMachine.stop()
        # sigterm_handler(signal.SIGTERM, 0)
