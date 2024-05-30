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
        Config.open()

    def open(name="default.ini"):
        logger.debug('opening ' + name)
        Config.save()
        Config.currentConfig = name
        path = Config.configFolder + name
        if os.path.exists(path):
            logger.info('opening config ' + name)
            Config.__config.read(path)
            if not (Config.__getint('Metadata', 'Version') == '0'):
                logger.warn("Config %s is outdated!", name)
                Config.__loadDefault()
        else:
            logger.info('no config exists, opening default')
            Config.__loadDefault()
            Config.save()

    def save():
        if Config.currentConfig == "":
            logger.debug("Attempting to save default config")
            return
        logger.info("Saving config: " + Config.currentConfig)

        path = Config.configFolder + Config.currentConfig
        if os.path.exists(path):
            logger.debug('removing old config')
            os.remove(path)

        logger.debug('writing new config')
        with open(path, 'w') as configfile:
            Config.__config.write(configfile)

    def getBeltSpeed() -> int:
        return Config.__getint('Belt', 'speed')

    def setBeltSpeed(speed):
        Config.__config['Belt']['speed'] = str(speed)
        Config.save()

    def getBeltDirection() -> int:
        return Config.__config['Belt'].get('direction', 'forward')

    def setBeltDirection(direction):
        Config.__config['Belt']['direction'] = str(direction)
        Config.save()

    def getLoadcell(type):
        if type not in ['lowValue', 'lowWeight', 'highValue', 'highWeight']:
            logger.error('Tried to get wrong loadcell type: %s', type)
            return
        return Config.__getint('Loadcell', type)

    def setLoadcell(type, value):
        if type not in ['lowValue', 'lowWeight', 'highValue', 'highWeight']:
            logger.error('Tried to set wrong loadcell type: %s', type)
            return
        Config.__config['Loadcell'][type] = value
        Config.save()

    def getWebPort() -> int:
        logger.debug('getting web port')
        return Config.__getint('WebConfig', 'port')

    def __createDefault():
        logger.debug('loading default')
        Config.__default = configparser.ConfigParser()
        Config.__default['Metadata'] = {'version': '2'}
        Config.__default['WebConfig'] = {'port': '8080',
                                         'address': ''}
        Config.__default['Belt'] = {'speed': '200',
                                    'direction': 'forward'}
        Config.__default['Loadcell'] = {'lowValue': '8000000',
                                        'lowWeight': '0',
                                        'highValue': '10000000',
                                        'highWeight': '1000'}
        logger.debug(Config.__default)

    def __loadDefault():
        Config.__config = Config.__default
        Config.currentConfig = 'default.ini'

    def __getint(section, name) -> int:
        logger.debug("getting value %s from config %s",
                     name, Config.currentConfig)
        default = Config.__default[section].getint(name)
        if Config.__config.has_section(section):
            return Config.__config[section].getint(name, fallback=default)
        else:
            return default
