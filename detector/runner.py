# coding: utf-8
from preparer import prepare
from searcher import init, match
from db import getAllLogos
from serializer import unserialize

class Result(object):
    def __init__(self, logoId, logoImg):
        self.logoId = logoId 
        self.logoImg = logoImg 

def runAll (imgPath, N):
    '''
    Поиск в изображении image логотипов
    возвращает первые N самых релевантных логотипов
    
    :param imgPath - путь до изображения, в котором будет производится поиск логотипов
    :param N - количество возвращаемых логотипов
    
    :return [<Result>, ...]
    '''
    detector, matcher = init('sift', False)
    kp2, desc2 = prepare(imgPath, detector, 960, 720)
    logoObjects = getAllLogos()
    bestLogoObjectByCompany = None
    bestLogoObjects = {}
    for logoObject in logoObjects:
        kp1, desc1 = getSearialData(logoObject['kpFileName'],logoObject['descFileName'])
        result = match(kp1, desc1, kp2, desc2, detector, matcher)
        logoObject['result'] = result
        logoObject['runk'] = getRunk(logoObject['result']['inliers'], logoObject['result']['matched'])
        if bestLogoObjectByCompany:
            if logoObject['companyId'] == bestLogoObjectByCompany['companyId']:
                if logoObject['runk'] > bestLogoObjectByCompany['runk']:
                    bestLogoObjectByCompany = logoObject
            else:
                bestLogoObjects.append(bestLogoObjectByCompany)
                bestLogoObjectByCompany = logoObject
        else:
            bestLogoObjectByCompany = logoObject
            

def getSearialData(kpFileName, descFileName):
    '''
    Получить подготовленные данные о изображении/логотипе по его 
    
    :param imgPath - путь до изображения, в котором будет производится поиск логотипов
    :param N - количество возвращаемых логотипов
    
    :return [<Result>, ...]
    '''
    return unserialize(kpFileName), unserialize(descFileName)

def addResult(logoObjects, logoObject, N):
    '''
    Добавление в массив результатов. В массиве результатов всегда должно быть не более N элементов
    
    :param inliers
    :param matched
    
    :result runk
    '''
  TODOOOOOOOOOOOOOOOOOO!!!!!
    if not N or N <= 0:
        raise Exception("runner.addResult: invalid N!")
    if len(logoObjects) == 0:
        logoObjects[1] = logoObject
    else:
        done = 0
        for i in range(1,len(logoObjects)):
            if logoObjects[i]['runk'] <= logoObjects[i]['runk']:
                logoObjects[i]
            else
            
def getRunk(inliers, matched):
    '''
    Функция, по значению которой производится сортировка результатов
    
    :param inliers
    :param matched
    
    :result runk
    '''
    if inliers and matched:
        return inliers * matched
    return 0
    


