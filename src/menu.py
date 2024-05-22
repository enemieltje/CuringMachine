from curingMachine import CuringMachine
from lib.esp8266_i2c_lcd import I2cLcd  # Example LCD interface used
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
        startBelt = MenuAction("Start", CuringMachine.startBelt)
        stopBelt = MenuAction("Stop", CuringMachine.stopBelt)

        beltMenu.add_option(startBelt)
        beltMenu.add_option(stopBelt)
        LcdMenu.menu.add_option(beltMenu)

        camMenu = Menu("Camera")
        picture = MenuAction("Take Picture", CuringMachine.picture)
        startCam = MenuAction("Start Cam", CuringMachine.startCam)
        stopCam = MenuAction("Stop Cam", CuringMachine.stopCam)

        camMenu.add_option(picture)
        camMenu.add_option(startCam)
        camMenu.add_option(stopCam)
        LcdMenu.menu.add_option(camMenu)

        ipMenu = MenuNoop(str(os.system('hostname -I')))
        LcdMenu.menu.add_option(ipMenu)

    def start():
        logger.debug("start")

        i2c = busio.I2C(board.SCL, board.SDA)

        # i2c = I2C(scl=Pin(3), sda=Pin(2), freq=400000)
        lcd = I2cLcd(i2c, 0x27, 4, 20)
        lcd.clear()

        LcdMenu.create()
        LcdMenu.menu.start(lcd)
