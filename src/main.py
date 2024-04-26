#!../.venv/bin/python
from belt import Belt
from server import Server
from camera import Camera
# The client class will start the program and contain all its components


class Client:
    belt: Belt
    server: Server
    camera: Camera

    # init is called when an instance of this class is created
    def __init__(self):
        print("start")
        self.camera = Camera()
        self.camera.startStream()
        self.server = Server()
        self.server.startStreamServer()
        self.camera.stopStream()
        self.belt = Belt()


# Create an instance of the Client class, and save it in a variable called client
if __name__ == "__main__":
    client = Client()
