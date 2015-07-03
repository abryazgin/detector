# -*- coding: utf-8 -*-
from web.lightsite import models
'''
Модуль, отвечающий за получение данных из БД
'''

def getAllLogos ():
    '''
    :returns ({'companyId'  : companyId,
               'logoId'     : logoId,
               'kpFileName' : kpFileName, 
               'kpFileName' : kpFileName
              }, ...)
              
              !!! ДОЛЖЕН БЫТЬ ОТСОРТИРОВАН ПО  companyId !!!
    '''
    return models.CompanyLogo.objects.order_by('company')