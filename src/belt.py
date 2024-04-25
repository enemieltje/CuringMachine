import gpiozero as GPIO
import time
from DRV8825 import DRV8825


class Belt:
    motor1: DRV8825
    motor2: DRV8825

    # init is called when an instance of this class is created
    def __init__(self):
        self.motor1 = DRV8825(dir_pin=13, step_pin=19,
                              enable_pin=12, mode_pins=(16, 17, 20))
        self.motor2 = DRV8825(dir_pin=24, step_pin=18,
                              enable_pin=4, mode_pins=(21, 22, 27))

        time.sleep(1)
        self.setupMotor(self.Motor1)
        time.sleep(2)
        self.setupMotor(self.Motor2)

    def setupMotor(self, motor: DRV8825):
        motor.SetMicroStep('softward', 'fullstep')
        motor.TurnStep(Dir='forward', steps=200, stepdelay=0.005)
        time.sleep(0.5)
        motor.TurnStep(Dir='backward', steps=400, stepdelay=0.005)
        motor.Stop()
