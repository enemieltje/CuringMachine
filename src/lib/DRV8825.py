import multiprocessing
import gpiozero as GPIO
import time
import logging

logger = logging.getLogger(__name__)

# This is a library for our motor drive HAT (with the DRV8825 chip) that I imported as a file.

MotorDir = [
    'forward',
    'backward',
]

ControlMode = [
    'hardward',
    'softward',
]


class DRV8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):

        self.mode_pins = mode_pins
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.step_pin = step_pin

        self.dir = GPIO.LED(self.dir_pin)
        self.step = GPIO.LED(self.step_pin)
        self.enable = GPIO.LED(self.enable_pin)
        self.mode_1 = GPIO.LED(self.mode_pins[0])
        self.mode_2 = GPIO.LED(self.mode_pins[1])
        self.mode_3 = GPIO.LED(self.mode_pins[2])

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)
        # GPIO.setup(self.dir_pin, GPIO.OUT)
        # GPIO.setup(self.step_pin, GPIO.OUT)
        # GPIO.setup(self.enable_pin, GPIO.OUT)
        # GPIO.setup(self.mode_pins, GPIO.OUT)
        self.control_pin = {
            dir_pin: self.dir,
            enable_pin: self.enable,
            step_pin: self.step,
            mode_pins[0]: self.mode_1,
            mode_pins[1]: self.mode_2,
            mode_pins[2]: self.mode_3
        }

        self.process = None
        self.keepTurning = False
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

    def digital_write(self, pin, value):
        if value:
            self.control_pin[pin].on()
        else:
            self.control_pin[pin].off()

        # GPIO.output(pin, value)

    def Stop(self):
        self.keepTurning = False
        self.parent_conn.send(False)
        self.process.kill()
        self.digital_write(self.enable_pin, 0)

    def Configure_mode(self, microstep):
        j = 0
        for i in microstep:
            self.digital_write(self.mode_pins[j], i)
            j = j+1

    def SetMicroStep(self, mode, stepformat):
        """
        (1) mode
            'hardward' :    Use the switch on the module to control the microstep
            'software' :    Use software to control microstep pin levels
                Need to put the All switch to 0
        (2) stepformat
            ('fullstep', 'halfstep', '1/4step', '1/8step', '1/16step', '1/32step')
        """
        microstep = {'fullstep': (0, 0, 0),
                     'halfstep': (1, 0, 0),
                     '1/4step': (0, 1, 0),
                     '1/8step': (1, 1, 0),
                     '1/16step': (0, 0, 1),
                     '1/32step': (1, 0, 1)}

        logger.debug("Control mode:", mode)
        if (mode == ControlMode[1]):
            logger.debug("set pins")
            # self.digital_write(self.mode_pins, microstep[stepformat])
            self.Configure_mode(microstep[stepformat])

    def TurnStep(self, Dir, steps=0, stepdelay=0.005):
        logger.debug("starting motor with stepdelay %i", stepdelay)
        if (Dir == MotorDir[0]):
            logger.debug("forward")
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 0)
        elif (Dir == MotorDir[1]):
            logger.debug("backward")
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 1)
        else:
            logger.warn("the dir must be : 'forward' or 'backward'")
            self.digital_write(self.enable_pin, 0)
            return

        if (steps == 0):
            self.process = multiprocessing.Process(
                target=self.__TurnIndefinite, args=([stepdelay]))
            self.parent_conn.send(True)
            self.process.start()
            # self.__TurnIndefinite(stepdelay)

        logger.debug("turn step:" + steps)
        for i in range(steps):
            self.digital_write(self.step_pin, True)
            time.sleep(stepdelay)
            self.digital_write(self.step_pin, False)
            time.sleep(stepdelay)

    def __TurnIndefinite(self, stepdelay=0.005):
        if self.keepTurning:
            logger.warn("Motor is already running")
            return
        self.keepTurning = True
        count1 = time.perf_counter()

        # recv = self.child_conn.recv()
        while True:
            self.digital_write(self.step_pin, True)
            count2 = time.perf_counter()
            steptime = float(count2 - count1)
            logger.debug("step time1: " + str(steptime))
            # logger.debug("wait time: " + str(stepdelay - steptime))
            if stepdelay > steptime:
                time.sleep(stepdelay - steptime)
            else:
                logger.warn('step took too long')

            self.digital_write(self.step_pin, False)
            count1 = time.perf_counter()
            steptime = float(count1 - count2)
            logger.debug("step time2: " + str(steptime))
            # logger.debug("wait time: " + str(stepdelay - steptime))
            if stepdelay > steptime:
                time.sleep(stepdelay - steptime)
            else:
                logger.warn('step took too long')

            # if self.child_conn.poll():
            #     recv = self.child_conn.recv()
