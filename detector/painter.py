# -*- coding: utf-8 -*-
import numpy as np
import cv2


def drawMatch(img1, img2, kpPairs, status=None, H=None):
    '''
    Отрисовка совпадений двух изображений
    
    :param img1 - первое изображение
    :param img2 - второе изображение
    :param kpPairs - совпадения
    :param status - ?
    :param H - ?
    
    :returns <Image>
    '''
    green = (0, 255, 0)
    red = (0, 0, 255)
    white = (255, 255, 255)
    
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
    vis[:h1, :w1] = img1
    vis[:h2, w1:w1+w2] = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        cv2.polylines(vis, [corners], True, white)

    if status is None:
        status = np.ones(len(kpPairs), np.bool_)
    p1 = np.int32([kpp[0].pt for kpp in kpPairs])
    p2 = np.int32([(kpp[1].pt[0] + w1,kpp[1].pt[1]) for kpp in kpPairs]) #+ (w1, 0)

    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            col = green
            cv2.circle(vis, (x1, y1), 2, col, -1)
            cv2.circle(vis, (x2, y2), 2, col, -1)
        else:
            col = red
            r = 2
            thickness = 3
            cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
            cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)
    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            cv2.line(vis, (x1, y1), (x2, y2), green)

    return vis
