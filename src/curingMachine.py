import logging
import multiprocessing
from belt import Belt
from camera import Camera

logger = logging.getLogger(__name__)


class CuringMachine():
    # This class serves as an interface between all components of the machine
    cameras = list()

    def showcase():
        # Show that the motors are operational
        logger.debug("showcase")

        # Start the belt showcase as a separate process so that it does not freeze the webpage
        # process = multiprocessing.Process(target=Belt.showcase)
        # process.start()
        Belt.start()

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
        # TODO: Do this in a separate process
        # TODO: Check if the file exists already to avoid overwriting old pictures
        logger.debug("picture")
        return CuringMachine.cameras[index].picture()

    def addCamera(camera: Camera):
        logger.debug('adding camera')
        CuringMachine.cameras.append(camera)

    def start():
        # add all the cameras and start the web server
        logger.debug('starting curing machine')
        CuringMachine.addCamera(Camera())

    def stop():
        # stop all the cameras and the web server
        # TODO: stop stepper motors
        for camera in CuringMachine.cameras:
            camera.stopStream()
