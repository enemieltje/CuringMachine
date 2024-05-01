import logging
import multiprocessing
from config import Config
import time
from DRV8825 import DRV8825

logger = logging.getLogger(__name__)


class Belt:
    # The belt contains two motors with different pins
    motors = list()

    def configure():
        Belt.motors.append(DRV8825(dir_pin=13, step_pin=19,
                                   enable_pin=12, mode_pins=(16, 17, 20)))
        Belt.motors.append(DRV8825(dir_pin=24, step_pin=18,
                                   enable_pin=4, mode_pins=(21, 22, 27)))
        for motor in Belt.motors:
            motor.SetMicroStep('hardward', '1/4step')

    def showcase():
        # Show that the motors are active by turning them a bit
        time.sleep(1)
        Belt.showcaseMotor(Belt.motors[0])
        time.sleep(2)
        Belt.showcaseMotor(Belt.motors[1])

    def showcaseMotor(motor: DRV8825):
        motor.TurnStep(Dir='forward', steps=200, stepdelay=0.005)
        time.sleep(0.5)
        motor.TurnStep(Dir='backward', steps=400, stepdelay=0.005)
        motor.Stop()

    def start():
        logger.debug("starting belt")
        process1 = multiprocessing.Process(
            target=Belt.startMotor, args=([0]))
        process2 = multiprocessing.Process(
            target=Belt.startMotor, args=([1]))
        process1.start()
        process2.start()

    def startMotor(index):
        speed = Config.getBeltSpeed()
        logger.debug("starting motor with speed %i", speed)
        motor = Belt.motors[index]
        motor.TurnStep(Dir='forward', steps=200, stepdelay=1/speed)


Belt.configure()
