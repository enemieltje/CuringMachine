from gpiozero import Button
import logging
from menu import LcdMenu

logger = logging.getLogger(__name__)


class Input():
    bounce_time = 0.2
    up = Button(11, pull_up=False, bounce_time=bounce_time)
    down = Button(26, pull_up=False, bounce_time=bounce_time)
    left = Button(15, pull_up=False, bounce_time=bounce_time)
    right = Button(23, pull_up=False, bounce_time=bounce_time)
    ok = Button(14, pull_up=False, bounce_time=bounce_time)
    power = Button(25, pull_up=False, bounce_time=bounce_time)

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
        LcdMenu.menu = LcdMenu.menu.parent()

    def pressRight():
        logger.debug("right")
        LcdMenu.menu = LcdMenu.menu.choose()

    def pressOk():
        logger.debug("ok")
        LcdMenu.menu = LcdMenu.menu.choose()

    def pressPower():
        logger.debug("power")
