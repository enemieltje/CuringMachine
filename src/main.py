#!../.venv/bin/python
from belt import Belt
from server import Server
from camera import Camera


# Create an instance of the Client class, and save it in a variable called client
if __name__ == "__main__":
    print("start")
    camera = Camera()
    Server.addCamera(camera)
    Server.startStreamServer()
    belt = Belt()
