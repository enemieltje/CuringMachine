import gpiozero as GPIO
import time
from DRV8825 import DRV8825


class Belt:
    motor1 = DRV8825(dir_pin=13, step_pin=19,
                     enable_pin=12, mode_pins=(16, 17, 20))
    motor2 = DRV8825(dir_pin=24, step_pin=18,
                     enable_pin=4, mode_pins=(21, 22, 27))

    # init is called when an instance of this class is created

    def showcase():
        time.sleep(1)
        Belt.setupMotor(Belt.motor1)
        time.sleep(2)
        Belt.setupMotor(Belt.motor2)

    def setupMotor(motor: DRV8825):
        motor.SetMicroStep('hardward', '1/4step')
        motor.TurnStep(Dir='forward', steps=200, stepdelay=0.005)
        time.sleep(0.5)
        motor.TurnStep(Dir='backward', steps=400, stepdelay=0.005)
        motor.Stop()
