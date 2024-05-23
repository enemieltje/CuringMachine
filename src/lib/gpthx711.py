import time
from gpiozero import DigitalInputDevice, DigitalOutputDevice

class HX711:
    def __init__(self, dout_pin, pd_sck_pin, gain=128):
        self.PD_SCK = DigitalOutputDevice(pd_sck_pin)
        self.DOUT = DigitalInputDevice(dout_pin)
        self.GAIN = 0
        self.REFERENCE_UNIT = 1
        self.offset = 0

        self.set_gain(gain)

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

        self.PD_SCK.off()
        self.read()

    def is_ready(self):
        return self.DOUT.is_active == False

    def read(self):
        while not self.is_ready():
            pass

        count = 0
        for _ in range(24):
            self.PD_SCK.on()
            count = count << 1
            self.PD_SCK.off()
            if self.DOUT.is_active:
                count += 1

        self.PD_SCK.on()
        count = count ^ 0x800000
        self.PD_SCK.off()

        for _ in range(self.GAIN):
            self.PD_SCK.on()
            self.PD_SCK.off()

        return count

    def read_average(self, times=3):
        values = 0
        for _ in range(times):
            values += self.read()
        return values / times

    def get_value(self, times=3):
        return self.read_average(times) - self.offset

    def get_weight(self, times=3):
        value = self.get_value(times)
        return value / self.REFERENCE_UNIT

    def tare(self, times=15):
        self.offset = self.read_average(times)

    def set_reference_unit(self, reference_unit):
        self.REFERENCE_UNIT = reference_unit

    def power_down(self):
        self.PD_SCK.off()
        self.PD_SCK.on()
        time.sleep(0.0001)

    def power_up(self):
        self.PD_SCK.off()
        self.read()

if __name__ == "__main__":
    dout_pin = 5
    pd_sck_pin = 6

    hx = HX711(dout_pin, pd_sck_pin)
    hx.set_reference_unit(92)
    hx.tare()

    print("Tare done! Add weight now...")

    try:
        while True:
            weight = hx.get_weight(5)
            print("Weight: {} grams".format(weight))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
