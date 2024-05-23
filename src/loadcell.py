from lib.gpthx711 import HX711
import logging
import time

logger = logging.getLogger(__name__)


class Loadcell():

    def start():
        Loadcell.hx = HX711(5, 6)
        Loadcell.hx.set_reference_unit(92)
        Loadcell.hx.tare()

    def print():
        weight = Loadcell.hx.get_weight(5)
        logger.info("Weight: {} grams".format(weight))
        time.sleep(1)
