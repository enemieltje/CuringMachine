import configparser
import os
import logging

logger = logging.getLogger(__name__)


class Config():
    configFolder = "config/"
    currentConfig = ""
    __config = configparser.ConfigParser()
    __default = configparser.ConfigParser()

    def start():
        Config.__createDefault()

    def open(name="default.ini"):
        Config.save()
        Config.currentConfig = name
        path = Config.configFolder + name
        if os.path.exists(path):
            Config.__config.read(path)
            if not (Config.__getint('Version') == '0'):
                logger.warn("Config %s is outdated!", name)
                Config.__loadDefault()
                Config.currentConfig = ''
        else:
            Config.__loadDefault()
            Config.save()

    def save():
        if Config.currentConfig == "":
            logger.debug("Attempting to save default config")
            return
        logger.info("Saving config: " + Config.currentConfig)
        Config.__config.write(Config.currentConfig)

    def getBeltSpeed() -> int:
        return Config.__getint('Parameters.beltSpeed')

    def getWebPort() -> int:
        return Config.__getint('WebConfig.port')

    def __createDefault():
        Config.__default = configparser.ConfigParser()
        Config.__default['Version'] = '0'
        Config.__default['WebConfig'] = {'port': '8080',
                                         'address': ''}
        Config.__default['Parameters'] = {'beltSpeed': '10'}

    def __loadDefault():
        Config.__config = Config.__default

    def __getint(name) -> int:
        logger.debug("getting value %s from config %s",
                     name, Config.currentConfig)
        default = Config.__default.getint(name)
        return Config.__config.getint(name, default)


Config.start()
