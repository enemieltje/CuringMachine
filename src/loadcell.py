from lib.hx711 import HX711
import logging
import time

logger = logging.getLogger(__name__)


class Loadcell():

    def start():
        # Loadcell.hx = HX711(5, 6)
        Loadcell.hx = HX711(dout_pin=5, pd_sck_pin=6, gain=128, channel='A')
        Loadcell.reset()

    def reset():
        logger.debug("Reset")
        result = Loadcell.hx.reset()		# Before we start, reset the hx711 ( not necessary)
        if result:			# you can check if the reset was successful
            logger.info('Ready to use')
        else:
            logger.warn('not ready')

    def print():
        data = Loadcell.hx.get_raw_data(5)

        if data != False:  # always check if you get correct value or only False
            logger.info('Raw data: ' + str(data))
        else:
            logger.info('invalid data')
