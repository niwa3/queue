#!/usr/bin/python3
# coding: UTF-8
import simpy 
import myQueue as qu
import myGenerater as ge

'''
class MyEnv
To extend the simpy.Environment class.
'''
class MyEnv(simpy.Environment):
    def __init__(self):
        super().__init__()
        self._nextClassId = 1
        self._classIdIndex = {}

    def MGenerater(self, generaterId, mean, className=None):
        classId = 0
        if className is not None:
            classId = self._classIdIndex[className]
        generater = ge.MGenerater(self, generaterId, mean, classId)
        return generater

    def DGenerater(self, generaterId, mean, className=None):
        classId = 0
        if className is not None:
            classId = self._classIdIndex[className]
        generater = ge.DGenerater(self, generaterId, mean, classId)
        return generater

    def MFQueue(self, queueId, mean):
        queue = qu.MFQueue(self, queueId, mean)
        return queue

    def DFQueue(self, queueId, mean):
        queue = qu.DFQueue(self, queueId, mean)
        return queue

    def MPQueue(self, queueId, mean):
        queue = qu.MPQueue(self, queueId, mean)
        return queue

    def DPQueue(self, queueId, mean):
        queue = qu.DPQueue(self, queueId, mean)
        return queue

    def newClass(self, className):
        self._classIdIndex[className] = self._nextClassId
        return self._classIdIndex[className]

    def getClassList(self):
        return self._classIdIndex
