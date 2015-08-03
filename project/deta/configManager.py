# -*- coding: utf-8 -*-

'''
Модуль, отвечающий за работу с конфигурационным файлом проекта

Использование:

    from configManager import Config
  
    Config.get(<БЛОК КОНФИГА>, <НАЗВАНИЕ ПАРАМЕТРА>)
'''

import ConfigParser
import os

Config = ConfigParser.ConfigParser()

fileConfig = (os.path.join(os.getcwd(),'config'))
Config.read(fileConfig)