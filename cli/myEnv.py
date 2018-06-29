#!/usr/bin/python3
# coding: UTF-8
import simpy 
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
        self._action = self.process(self.loop())

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

    def loop(self):
        while True:
            yield self.timeout(1)
            sys.stdout.write('\r\033[K' + '%d >>>' % self.now)
            sys.stdout.flush()

if __name__ == '__main__':
    env = MyEnv()
    env.newClass('a')

    g1_1 = env.MGenerater('g1_1', 10, 'a')
    g1_2 = env.MGenerater('g1_2', 10)

    g2_1 = env.MGenerater('g2_1', 10, 'a')
    g2_2 = env.MGenerater('g2_2', 10)

    q1_1 = env.DPQueue('q1_1', 3)
    q1_1.assignClass('a')

    q1_2 = env.DPQueue('q1_2', 3)

    q2 = env.DPQueue('q2', 3)
    q2.assignClass('a')

    g1_1.nextQueue = q1_1
    g1_2.nextQueue = q1_1

    g2_1.nextQueue = q1_2
    g2_2.nextQueue = q1_2

    q1_1.nextQueue = q2
    q1_2.nextQueue = q2

    env.run()

    print('')
