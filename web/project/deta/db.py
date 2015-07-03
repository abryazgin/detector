# -*- coding: utf-8 -*-
from lightsite import models
'''
Модуль, отвечающий за получение данных из БД
'''

def getAllLogos ():
    '''
    :returns ({'companyId'    : companyId,
               'logoId'       : logoId,
               'photoPath'    : logoPhotoPath
               'kpFilePath'   : kpFileName, 
               'descFilePath' : descFilePath
              }, ...)
              
              !!! ДОЛЖЕН БЫТЬ ОТСОРТИРОВАН ПО  companyId !!!
    '''
        
    return [{'companyId'   : logo.company.id,
             'logoId'      : logo.id,
             'photoPath'   : logo.photo.path,
             'kpFilePath'  : logo.serial_kp_file.path,
             'descFilePath': logo.serial_desc_file.path} for logo in models.CompanyLogo.objects.all().order_by('company') if logo.serial_kp_file and logo.serial_desc_file]