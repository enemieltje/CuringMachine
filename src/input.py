from gpiozero import Button
import logging
from menu import LcdMenu

logger = logging.getLogger(__name__)


class Input():

    up = Button(11)
    down = Button(26)
    left = Button(14)
    right = Button(15)
    ok = Button(23)
    power = Button(25)

    def start():
        logger.debug("start")
        Input.up.when_activated = Input.pressUp
        Input.down.when_activated = Input.pressDown
        Input.left.when_activated = Input.pressLeft
        Input.right.when_activated = Input.pressRight
        Input.ok.when_activated = Input.pressOk
        Input.power.when_activated = Input.pressPower

    def pressUp():
        logger.debug("up")
        LcdMenu.menu.focus_prev()

    def pressDown():
        logger.debug("down")
        LcdMenu.menu.focus_next()

    def pressLeft():
        logger.debug("left")
        LcdMenu.menu.parent()

    def pressRight():
        logger.debug("right")
        LcdMenu.menu.choose()

    def pressOk():
        logger.debug("ok")
        LcdMenu.menu.focus_prev()

    def pressPower():
        logger.debug("power")
        LcdMenu.menu.focus_prev()
