#!../.venv/bin/python
from belt import Belt
from server import Server
# The client class will start the program and contain all its components


class Client:
    belt: Belt
    server: Server

    # init is called when an instance of this class is created
    def __init__(self):
        print("start")
        self.server = Server()
        self.belt = Belt()


# Create an instance of the Client class, and save it in a variable called client
if __name__ == "__main__":
    client = Client()
