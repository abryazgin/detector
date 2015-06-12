# -*- coding: utf-8 -*-


#import pickle
from configManager import Config
from cv2 import KeyPoint

__KP_FLAG__ = '__LIST_OF_KEYPOINTS__'

def serialize (obj, filename, byCPickle = True):
    '''
    Сериализация объекта и сохранение в файл
    ''' 
    if byCPickle:
        import cPickle as pickle
    else:
        import pickle
    if isinstance(obj,list) and len(obj) > 0 and str(type(obj[0])) == "<type 'cv2.KeyPoint'>":
        obj = getSearializableObjFromListKP(obj)
    with open('/'.join((Config.get('PATHS', 'serialDir'),filename)), 'wb') as f:
        pickle.dump(obj, f)
  
def unserialize (filename, byCPickle = True):
    '''
    Загрузка из файла и рассериализация объекта
    Возвращаем объект
    '''
    if byCPickle:
        import cPickle as pickle
    else:
        import pickle
    with open('/'.join((Config.get('PATHS', 'serialDir'),filename)),'rb') as f:
        obj = pickle.load(f)
    if isinstance(obj,list) and len(obj) > 1 and obj[0] == __KP_FLAG__:
        return getListKPFromSearializedObj(obj)
    return obj

def getSearializableObjFromListKP(listOfKP):
    '''
    Подготовка сериализуемых данных из списка KeyPoint-ов
    '''
    return [__KP_FLAG__] + [ {'x'        : kp.pt[0],
                              'y'        : kp.pt[1],
                              'size'     : kp.size,
                              'angle'    : kp.angle,
                              'response' : kp.response,
                              'octave'   : kp.octave,
                              'class_id' : kp.class_id} for kp in listOfKP]

def getListKPFromSearializedObj(listOfKP):
    '''
    Возвращение из сериализованных данных списка KeyPoint-ов
    '''
    return [ KeyPoint(listOfKP[i]['x'],
                      listOfKP[i]['y'],
                      listOfKP[i]['size'],
                      listOfKP[i]['angle'],
                      listOfKP[i]['response'],
                      listOfKP[i]['octave'],
                      listOfKP[i]['class_id']) for i in range(1,len(listOfKP))]