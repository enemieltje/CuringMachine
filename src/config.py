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
        logger.debug('starting config')
        Config.__createDefault()

    def open(name="default.ini"):
        logger.debug('opening ' + name)
        Config.save()
        Config.currentConfig = name
        path = Config.configFolder + name
        if os.path.exists(path):
            Config.__config.read(path)
            if not (Config.__getint('Metadata', 'Version') == '0'):
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
        return Config.__getint('Parameters', 'beltSpeed')

    def getWebPort() -> int:
        logger.debug('getting web port')
        return Config.__getint('WebConfig', 'port')

    def __createDefault():
        logger.debug('loading default')
        Config.__default = configparser.ConfigParser()
        Config.__default['Metadata'] = {'version': '0'}
        Config.__default['WebConfig'] = {'port': '8080',
                                         'address': ''}
        Config.__default['Parameters'] = {'beltSpeed': '200'}
        logger.debug(Config.__default)

    def __loadDefault():
        Config.__config = Config.__default

    def __getint(section, name) -> int:
        logger.debug("getting value %s from config %s",
                     name, Config.currentConfig)
        default = Config.__default[section].getint(name)
        if Config.__config.has_section(section):
            return Config.__config[section].getint(name, fallback=default)
        else:
            return default


Config.start()
