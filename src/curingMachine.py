import logging
import multiprocessing
import sys
from belt import Belt
from camera import Camera
from config import Config
from input import Input
from loadcell import Loadcell
from menu import LcdMenu
from server import Server

logger = logging.getLogger(__name__)


class CuringMachine():
    # This class serves as an interface between all components of the machine
    cameras = list()

    def startBelt():
        logger.debug("start belt")

        Belt.start()

    def stopBelt():
        logger.debug("stop belt")

        Belt.stop()

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
        Config.start()
        CuringMachine.addCamera(Camera())
        Loadcell.start()
        Input.start()
        LcdMenu.start()
        Server.start()

    def stop():
        # Gracefully stop the server when the program exits or crashes
        # This makes sure to stop the cameras and unpower the steppers
        logger.info("stopping...")
        LcdMenu.lcd.move_to(0, 1)
        LcdMenu.lcd.putstr("Stopping...")

        for camera in CuringMachine.cameras:
            camera.stopStream()
        Belt.stop()
        Config.save()
        Server.stop()

        LcdMenu.lcd.clear()
        LcdMenu.lcd.backlight_off()
        sys.exit(0)
