# coding: utf-8
from preparer import prepare
from preparer import prepareByFile
from searcher import init, match
from db import getAllLogos, addLogoStatistic
from serializer import unserialize
from configManager import Config

class Result(object):
    def __init__(self, logoId, companyId, logoImg):
        self.logoId = logoId 
        self.companyId = companyId
        self.logoImg = logoImg
        
    def __unicode__(self):
        return '%s - %s - %s' % (self.logoId, self.companyId, self.logoImg)

def runAll (img, imgPath, N):
    '''
    Поиск в изображении image логотипов
    возвращает первые N самых релевантных логотипов по img или imgPath

    :param img - изображение, в котором будет производится поиск логотипов
    :param imgPath - путь до изображения, в котором будет производится поиск логотипов
    :param N - количество возвращаемых логотипов
    
    :return [<Result>, ...]
    '''
    if not img and not imgPath:
        raise Exception('img and imgPath is None')
    detector, matcher = init('sift', False)
    if imgPath :
        kp2, desc2 = prepare(imgPath, detector, Config.get('PHOTOS','w'), Config.get('PHOTOS','h'))
    else :
        kp2, desc2 = prepareByFile(img, detector, Config.get('PHOTOS','w'), Config.get('PHOTOS','h'))
    logoObjects = getAllLogos()
    bestLogoObjectByCompany = None
    bestLogoObjects = []
    for logoObject in logoObjects:
        print logoObject['photoPath']
        print 'GET SERIAL DATA' 
        kp1, desc1 = getSearialData(logoObject['kpFilePath'],logoObject['descFilePath'])
        print 'MATCHING'
        result = match(kp1, desc1, kp2, desc2, detector, matcher)
        print 'RESULT'
        print result
        logoObject['result'] = result
        logoObject['runk'] = getRunk(logoObject['result']['res'], logoObject['result']['inliers'], logoObject['result']['matched'])
        print 'RUNK = %s' % logoObject['runk']
        if not logoObject['runk'] == 0:
            if bestLogoObjectByCompany:
                if logoObject['companyId'] == bestLogoObjectByCompany['companyId']:
                    if logoObject['runk'] > bestLogoObjectByCompany['runk']:
                        bestLogoObjectByCompany = logoObject
                else:
                    addResult(bestLogoObjects, bestLogoObjectByCompany, N)
                    bestLogoObjectByCompany = logoObject
            else:
                bestLogoObjectByCompany = logoObject

    if bestLogoObjectByCompany:
        addResult(bestLogoObjects, bestLogoObjectByCompany, N)
    result = [Result(logo['logoId'],
                   logo['companyId'],
                   logo['photoPath']) for logo in bestLogoObjects]

    return result
            

def addLogoStatisticToDB(bestLogoObjects):
    '''
    Добавить результаты в БД
    
    :param bestLogoObjects: список результатов
    
    '''
    for i in range(len(bestLogoObjects)):
        result = bestLogoObjects[i]
        addLogoStatistic(result.logoId, i + 1)
  
def getSearialData(kpFilePath, descFilePath):
    '''
    Получить подготовленные данные о изображении/логотипе по названиям файлов с его сериализованными данными
    
    :param kpFilePath - путь до файла с сериализованным списком особых точек
    :param descFilePath - путь до файла с сериализованным описанием особых точек
    
    :return рассериализованные данные kp, desc
    '''
    return unserialize(kpFilePath), unserialize(descFilePath)

def addResult(logoObjects, logoObject, N):
    '''
    Добавление в массив результатов. В массиве результатов всегда должно быть не более N элементов
    
    :param logoObjects: список результатов
    :param logoObject: претендент на добавление в список результатов
    :param N: количество результатов в списке результатов
    
    ###:result <integer>: текущая позиция
    '''
    if not N or N <= 0:
        raise Exception("runner.addResult: invalid N!")
    count = len(logoObjects)
    print 'ALREADY: %s' % count
    for i in range(N):
        if count == i:
            print logoObjects
            print i
            logoObjects[i:i+1] = [logoObject]
            return # i
        if logoObjects[i]['runk'] < logoObject['runk']:
            lo = logoObjects[i]
            logoObjects[i] = logoObject
            logoObject = lo
            
def getRunk(res, inliers, matched):
    '''
    Функция, по значению которой производится сортировка результатов
    
    :param res: резуьтат (1 - успех, 0 - неудача)
    :param inliers
    :param matched
    
    :result runk
    '''
    if inliers and matched:
        return res * inliers * matched
    return 0
    


