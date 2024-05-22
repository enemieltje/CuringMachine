from curingMachine import CuringMachine
from lib.esp8266_i2c_lcd import I2cLcd  # Example LCD interface used
from upymenu import Menu, MenuAction, MenuNoop
import os

import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd


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

        ipMenu = MenuNoop(os.system('hostname -I'))
        LcdMenu.menu.add_option(ipMenu)

    def start(lcd):
        i2c = busio.I2C(board.SCL, board.SDA)
        lcd = character_lcd.Character_LCD_I2C(i2c, 4, 20)

        LcdMenu.create()
        LcdMenu.menu.start(lcd)
