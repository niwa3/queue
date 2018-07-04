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
        self._exit = []

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

    def GPQueue(self, queueId, mean, num=1):
        queue = qu.GPQueue(self, queueId, mean, num)
        return queue

    def newClass(self, className):
        self._classIdIndex[className] = self._nextClassId
        self._nextClassId += 1
        return self._classIdIndex[className]

    def getClassList(self):
        return self._classIdIndex

    def classNameToId(self, className):
        return self._classIdIndex[className]

    def exitTask(self, task):
        self._exit.append(task)


if __name__ == '__main__':
    env = MyEnv()

    g1_1 = env.MGenerater('g1_1', 5)

    q1_1 = env.GFQueue('q1_1', 3, 3)

    q2 = env.GFQueue('q2', 3)

    g1_1.nextQueue = q1_1

    q1_1.nextQueue = q2

    env.run(1000000)

    q1_1.printResult()
    q2.printResult()
