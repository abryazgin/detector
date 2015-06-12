# -*- coding: utf-8 -*-

'''
Модуль, отвечающий за работу с конфигурационным файлом проекта

Использование:

    from configManager import Config
  
    Config.get(<БЛОК КОНФИГА>, <НАЗВАНИЕ ПАРАМЕТРА>)
'''

import ConfigParser

Config = ConfigParser.ConfigParser()

Config.read('config')