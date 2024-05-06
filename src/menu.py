import Pin
import I2C  # Basics for creating an LCD interface
from curingMachine import CuringMachine
from lib.esp8266_i2c_lcd import I2cLcd  # Example LCD interface used
from upymenu import Menu, MenuAction, MenuNoop


class LcdMenu():

    menu = Menu("Main Menu")

    def create():
        beltMenu = Menu("Belt")
        showcase = MenuAction("Showcase", CuringMachine.showcase)
        disableStepper = MenuAction(
            "Disable Steppers", CuringMachine.disableSteppers)

        beltMenu.add_option(showcase)
        beltMenu.add_option(disableStepper)
        LcdMenu.menu.add_option(beltMenu)

        camMenu = Menu("Camera")
        picture = MenuAction("Take Picture", CuringMachine.picture)
        startCam = MenuAction("Start Cam", CuringMachine.startCam)
        stopCam = MenuAction("Stop Cam", CuringMachine.stopCam)

        camMenu.add_option(picture)
        camMenu.add_option(startCam)
        camMenu.add_option(stopCam)
        LcdMenu.menu.add_option(camMenu)

    def start(lcd):
        LcdMenu.start(lcd)
