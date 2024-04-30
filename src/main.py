#!../.venv/bin/python
from belt import Belt
from server import Server
from camera import Camera
import signal
import sys


def sigterm_handler(_signo, _stack_frame):
    print("stopping server...")
    Server.stop()
    sys.exit(0)


# Create an instance of the Client class, and save it in a variable called client
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    # signal.signal(signal.SIGKILL, sigterm_handler)

    print("start")
    camera = Camera()
    Server.addCamera(camera)
    try:
        Server.start()
    finally:
        sigterm_handler(signal.SIGTERM, 0)
