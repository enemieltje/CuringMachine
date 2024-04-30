import logging
import multiprocessing
from belt import Belt
from camera import Camera
from server import Server

logger = logging.getLogger(__name__)


class CuringMachine():
    # This class serves as an interface between all components of the machine
    cameras = list()

    def showcase():
        # Show that the motors are operational
        logger.debug("showcase")

        # Start the belt showcase as a separate process so that it does not freeze the webpage
        process = multiprocessing.Process(target=Belt.showcase)
        process.start()

    def startCam():
        # TODO: Allow starting/stopping a single camera?
        logger.debug("start cam")
        for camera in CuringMachine.cameras:
            camera.startStream()

    def stopCam():
        logger.debug("stop cam")
        for camera in CuringMachine.cameras:
            camera.stopStream()

    def picture(index=0):
        # Take a picture and send the imagestream directly to the webpage
        # TODO: Open this in a new tab
        logger.debug("picture")
        return CuringMachine.cameras[index].picture()

    def addCamera(camera: Camera):
        CuringMachine.cameras.append(camera)

    def start():
        # add all the cameras and start the web server
        CuringMachine.addCamera(Camera())
        Server.start()

    def stop():
        # stop all the cameras and the web server
        # TODO: stop stepper motors
        for camera in CuringMachine.cameras:
            camera.stopStream()
        Server.stop()
