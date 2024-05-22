from curingMachine import CuringMachine
from lib.i2c_lcd import I2cLcd  # Example LCD interface used
from upymenu import Menu, MenuAction, MenuNoop
import os
from rpi_lcd import LCD
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import logging

logger = logging.getLogger(__name__)


class LcdMenu():

    menu = Menu("Main Menu")

    def create():
        logger.debug("create")
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

        ipMenu = MenuNoop(os.system('hostname -I'))
        LcdMenu.menu.add_option(ipMenu)

    def start():
        logger.debug("start")
        # lcd = LCD()

        # lcd.text('Hello World!', 1)
        i2c = busio.I2C(3, 2)
        # lcd = character_lcd.Character_LCD_I2C(i2c, 4, 20)

        # i2c = I2C(scl=Pin(3), sda=Pin(2), freq=400000)
        lcd = I2cLcd(1, 0x27, 4, 20)

        LcdMenu.create()
        LcdMenu.menu.start(lcd)
