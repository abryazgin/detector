# -*- coding: utf-8 -*-

from configManager import Config
from searcher import init
from preparer import prepare
from serializer import serialize, unserialize
import os



class TestRunner(object):
    
    resDirectory = Config.get('PATHS', 'resDir')
    photoDirectory = Config.get('PATHS', 'photoDir')
    logoDirectory = Config.get('PATHS', 'logoDir')
    
    
    def __init__(self):
        self.detector, self.matcher = init('sift', False)
    
    def testPrepare(self, imgPath):
        kp, desc = prepare(imgPath, self.detector, 960, 720)
        print kp, desc
        print 'Preparing DONE'
        
    def testSerialize(self, imgPath):
        kp, desc = prepare(imgPath, self.detector, 960, 720)
        print 'Preparing DONE'
        print '... serialize kp'
        serialize(kp, 'test_serial_kp.pick')
        print '... serialize desc'
        serialize(desc, 'test_serial_desc.pick')
        print 'Serializing DONE'
        print '... unserialize kp'
        kp2 = unserialize('test_serial_kp.pick')
        print '... unserialize desc'
        desc2 = unserialize('test_serial_desc.pick')
        print 'Unserializing DONE'
    
    
          

if __name__ == '__main__':
    TR = TestRunner()
    #TR.testPrepare('/home/abryazgin/lEgOq46T2Yo.jpg')
    TR.testSerialize('/home/abryazgin/lEgOq46T2Yo.jpg')
