import signal
import sys
from config import Config
from curingMachine import CuringMachine
from lib.esp8266_i2c_lcd import I2cLcd
from lib.upymenu import Menu, MenuAction, MenuDisplayValue, MenuNoop, MenuValue
import os
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import logging

from loadcell import Loadcell
from server import Server

logger = logging.getLogger(__name__)


def exit():
    LcdMenu.stop()
    CuringMachine.stop()
    Server.stop()
    LcdMenu.turnOff()
    sys.exit(0)


class LcdMenu():

    lcd: I2cLcd
    menu = Menu("Main Menu")

    def create():
        logger.debug("create")
        beltMenu = Menu("Belt")
        startBelt = MenuAction("Start", CuringMachine.startBelt)
        stopBelt = MenuAction("Stop", CuringMachine.stopBelt)
        beltSpeed = MenuValue(
            "Set Belt Speed", Config.getBeltSpeed, Config.setBeltSpeed)

        beltMenu.add_option(startBelt)
        beltMenu.add_option(stopBelt)
        beltMenu.add_option(beltSpeed)

        camMenu = Menu("Camera")
        picture = MenuAction("Take Picture", CuringMachine.picture)
        startCam = MenuAction("Start Cam", CuringMachine.startCam)
        stopCam = MenuAction("Stop Cam", CuringMachine.stopCam)

        camMenu.add_option(picture)
        camMenu.add_option(startCam)
        camMenu.add_option(stopCam)

        loadMenu = Menu('Loadcell')
        print = MenuAction("print values", Loadcell.print)
        reset = MenuAction('reset loadcell', Loadcell.reset)
        show = MenuDisplayValue('read loadcell', Loadcell.read)
        loadMenu.add_option(print)
        loadMenu.add_option(reset)
        loadMenu.add_option(show)

        mainMenu = Menu('Main Menu')

        ip = str(os.popen('hostname -I').read())
        logger.debug(ip)
        ipMenu = MenuNoop(ip)
        exitMenu = MenuAction("Exit", exit)

        mainMenu.add_option(beltMenu)
        mainMenu.add_option(camMenu)
        mainMenu.add_option(loadMenu)
        mainMenu.add_option(ipMenu)
        mainMenu.add_option(exitMenu)

        LcdMenu.menu = mainMenu

    def start():
        logger.debug("start")

        i2c = busio.I2C(board.SCL, board.SDA)

        LcdMenu.lcd = I2cLcd(i2c, 0x27, 4, 20)

        LcdMenu.create()
        LcdMenu.menu.start(LcdMenu.lcd)
        LcdMenu.menu.focus_next()

    def stop():
        LcdMenu.lcd.move_to(0, 1)
        LcdMenu.lcd.putstr("Stopping...")

    def turnOff():
        LcdMenu.lcd.clear()
        LcdMenu.lcd.backlight_off()
