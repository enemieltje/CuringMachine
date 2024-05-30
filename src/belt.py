import logging
import multiprocessing
from config import Config
import time
from lib.DRV8825 import DRV8825

logger = logging.getLogger(__name__)


class Belt:
    # The belt contains two motors with different pins
    motors = list()

    def configure():
        # create each of the motors and set their microstep config
        Belt.motors.append(DRV8825(dir_pin=13, step_pin=19,
                                   enable_pin=12, mode_pins=(16, 17, 20)))
        Belt.motors.append(DRV8825(dir_pin=24, step_pin=18,
                                   enable_pin=4, mode_pins=(21, 22, 27)))
        for motor in Belt.motors:
            motor.SetMicroStep('hardward', '1/4step')

    def start():
        # start running the belt
        # TODO: start the belt continuously instead of 200 steps
        logger.debug("starting belt")

        # start a separate process for each of the motors so that we don't freeze the program
        process1 = multiprocessing.Process(
            target=Belt.startMotor, args=([0]))
        process2 = multiprocessing.Process(
            target=Belt.startMotor, args=([1]))
        process1.start()
        # process2.start()

    def startMotor(index=0):
        # start turning a single motor
        speed = Config.getBeltSpeed()
        # direction = Config.getBeltDirection()
        direction = 'forward'
        logger.debug("starting motor with speed %i", speed)
        motor = Belt.motors[index]
        motor.TurnStep(Dir=direction, steps=0, stepdelay=1/speed)
        # motor.Stop()

    def stop():
        # stop each of the motors
        logger.info('stopping motors')
        for motor in Belt.motors:
            motor.Stop()


Belt.configure()
