# -*- coding: utf-8 -*-


import numpy as np
import cv2


def init(detectorName = 'sift', flann = False):
    '''
    Инициализация detector-а и matcher-а
    
    :param detectorName - название инициализируемого детектора (sift, surf, orb)
    :param flann - флаг (T/F) использовать ли алгоритм Фланна 
    '''
    if detectorName == 'sift':
        detector = cv2.SIFT()
        norm = cv2.NORM_L2
    elif detectorName == 'surf':
        detector = cv2.SURF(800)
        norm = cv2.NORM_L2
    elif detectorName == 'orb':
        detector = cv2.ORB(400)
        norm = cv2.NORM_HAMMING
    else:
        raise Exception('Invalid detector name')
    if flann:
        if norm == cv2.NORM_L2:
            flann_params = dict(algorithm = 1, trees = 5)
        else:
            flann_params= dict(algorithm = 6, table_number = 6, key_size = 12, multi_probe_level = 1)
        matcher = cv2.FlannBasedMatcher(flann_params, {})
    else:
        matcher = cv2.BFMatcher(norm)
    return detector, matcher  

def match(kp1, desc1, kp2, desc2, detector, matcher):
    '''
    Сравнение подготовленных данных логотипа (1) и изображении (2) 
    
    :param kp1      - особые точки логотипа
    :param desc1    - описания особых точек логотипа
    :param kp2      - особые точки изображения
    :param desc2    - описания особых точек изображения
    :param detector - детектор
    :param matcher  - сравниватель
    
    :returns  {'res'     : res, 
               'inliers' : inliers, 
               'matched' : matched}
    '''
    raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2) #2
    p1, p2, kpPairs = filterMatches(kp1, kp2, raw_matches)
    if len(p1) >= 4:
        H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
        print '%d / %d  inliers/matched' % (np.sum(status), len(status))
        result = {'res' : 1, 'inliers' : np.sum(status), 'matched' : len(status)}
    else:
        H, status = None, None
        print '%d matches found, not enough for homography estimation' % len(p1)
        result = {'res' : 0, 'inliers' : 0, 'matched' : 0}
    return result
  
def filterMatches( kp1, kp2, matches, ratio = 0.7):
    '''
    Фильтрация совпадений
    
    :param kp1 - набор точек первого изображения
    :param kp2 - набор точек второго изображения
    :param matches - совпадения 
    :param ratio - ?максимальное искажение?
    
    :returns p1, p2, kpPairs
    '''
    mkp1, mkp2 = [], []
    """
    max = 0
    min = 1000
    for m in matches:
        for i in m:
            if i.distance > max:
                max = i.distance
            elif i.distance < min:
                min = i.distance
    """
    for m in matches:
        if len(m) == 2 and m[0].distance > 1 and m[0].distance < m[1].distance * ratio:
        #if len(m) == 2 and not mkp1. m[0].distance > 3 * min and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kpPairs = zip(mkp1, mkp2)
    return p1, p2, kpPairs

        
