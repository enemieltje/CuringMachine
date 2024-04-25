#!../.venv/bin/python
from belt import Belt
# The client class will start the program and contain all its components


class Client:
    belt: Belt

    # init is called when an instance of this class is created
    def __init__(self):
        print("start")
        self.belt = Belt()


# Create an instance of the Client class, and save it in a variable called client
client = Client()
