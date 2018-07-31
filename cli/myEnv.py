#!/usr/bin/python3
# coding: UTF-8
import simpy
import numpy as np
import myQueue as qu
import myGenerater as ge
import sys

'''
class MyEnv
To extend the simpy.Environment class.
'''


class MyEnv(simpy.Environment):
    def __init__(self):
        super().__init__()
        self._nextClassId = 1
        self._classIdIndex = {}
        self._exit = []
        # self._printAction = self.process(self.showLoopNum())

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

    def GGenerater(self, generaterId, mean, className=None):
        classId = 0
        if className is not None:
            classId = self._classIdIndex[className]
        generater = ge.GGenerater(self, generaterId, mean, classId)
        return generater

    def MFQueue(self, queueId, mean, num=1):
        queue = qu.MFQueue(self, queueId, mean, num)
        return queue

    def DFQueue(self, queueId, mean, num=1):
        queue = qu.DFQueue(self, queueId, mean, num)
        return queue

    def GFQueue(self, queueId, mean, num=1):
        queue = qu.GFQueue(self, queueId, mean, num)
        return queue

    def MPQueue(self, queueId, mean, num=1):
        queue = qu.MPQueue(self, queueId, mean, num)
        return queue

    def DPQueue(self, queueId, mean, num=1):
        queue = qu.DPQueue(self, queueId, mean, num)
        return queue

    def GPQueue(self, queueId, mean, var, num=1):
        queue = qu.GPQueue(self, queueId, mean, var, num)
        return queue

    def newClass(self, className):
        self._classIdIndex[className] = self._nextClassId
        self._nextClassId += 1
        return self._classIdIndex[className]

    def getClassList(self):
        return self._classIdIndex

    def classNameToId(self, className):
        return self._classIdIndex[className]

    def classIdToName(self, classId):
        name = [k for k, v in self._classIdIndex.items() if v == classId]
        return name[0]

    def exitTask(self, task):
        self._exit.append(task)

    def showLoopNum(self):
        while True:
            yield self.timeout(1)
            sys.stdout.write(
                '\r\33[K'+'%d>>> finished tasks:%d'
                % (self.now, len(self._exit))
            )
            sys.stdout.flush()

    def printResult(self):
        totalTimes = {}
        for i in list(self._classIdIndex):
            totalTimes[i] = []
        for i in self._exit:
            totalTimes[self.classIdToName(i.classId)].append(i)
        for i in list(self._classIdIndex):
            totalTimeOfClass = []
            for j in totalTimes[i]:
                totalTime = 0
                for k in j.getQueueIdList():
                    time = j.getExitTime(k) - j.getQueueArrivedTime(k)
                    totalTime += time
                totalTimeOfClass.append(totalTime)
            print(i+str(totalTimes[i][0].getQueueIdList()) +
                  ': total time = %.3f' % np.average(totalTimeOfClass))
