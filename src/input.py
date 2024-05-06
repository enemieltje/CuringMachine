from gpiozero import Button

from menu import LcdMenu


class Input():

    up = Button(11)
    down = Button(26)
    left = Button(14)
    right = Button(15)
    ok = Button(23)
    power = Button(25)

    def start():
        Input.up.when_activated = LcdMenu.menu.focus_prev
        Input.down.when_activated = LcdMenu.menu.focus_next
        Input.left.when_activated = LcdMenu.menu.parent
        Input.right.when_activated = LcdMenu.menu.choose
