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
    
def addLogoStatistic (logoId, pos):
    '''
    Сохранение результатов поиска
    
    @param: logoId - идентификатор companyLogo
    @param: position - позиция в результате
    '''
    l = models.CompanyLogo.objects.get(pk=logoId)
    if not l:
        raise Exception('Company logo with id = %s does not exists' % logoId)
    if not pos:
        raise Exception('Position can not be %s' % pos)
    row = models.LogoStatistic(logo=l, position=pos)
    row.save()