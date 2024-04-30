import gpiozero as GPIO
import time
from DRV8825 import DRV8825


class Belt:
    # The belt contains two motors with different pins
    motor1 = DRV8825(dir_pin=13, step_pin=19,
                     enable_pin=12, mode_pins=(16, 17, 20))
    motor2 = DRV8825(dir_pin=24, step_pin=18,
                     enable_pin=4, mode_pins=(21, 22, 27))

    def showcase():
        # Show that the motors are active by turning them a bit
        time.sleep(1)
        Belt.showcaseMotor(Belt.motor1)
        time.sleep(2)
        Belt.showcaseMotor(Belt.motor2)

    def showcaseMotor(motor: DRV8825):
        motor.SetMicroStep('hardward', '1/4step')
        motor.TurnStep(Dir='forward', steps=200, stepdelay=0.005)
        time.sleep(0.5)
        motor.TurnStep(Dir='backward', steps=400, stepdelay=0.005)
        motor.Stop()
