#!/usr/bin/python3
# coding: UTF-8
import random as rd
import myTask as t
from abc import ABCMeta, abstractmethod
import numpy as np


class Generater(metaclass=ABCMeta):
    def __init__(self, env, generaterId, classId=None):
        self._env = env
        self._action = env.process(self.run())
        self._nextQueue = None
        self._id = generaterId
        self._classId = classId
        self._timeList = []

    @property
    def nextQueue(self):
        return self._nextQueue

    @nextQueue.setter
    def nextQueue(self, queue):
        self._nextQueue = queue

    def _createTask(self):
        task = t.Task(self._classId or 0)
        return task

    @abstractmethod
    def _duration(self):
        pass

    def printResult(self):
        ave = np.average(self._timeList)
        var = np.var(self._timeList)
        text = '('+self._id+')'
        text += 'E(t):%.3f V(t):%.3f' % (ave, var)
        print(text)
        return self._timeList

    def run(self):
        while True:
            yield self._env.process(self._duration())
            self._nextQueue.addTask(self._createTask())


class MGenerater(Generater):
    def __init__(self, env, generaterId, mean, classId=None):
        super().__init__(env, generaterId, classId)
        self._mean = mean

    def _duration(self):
        t = round(rd.expovariate(1.0/self._mean), 3)
        self._timeList.append(t)
        yield self._env.timeout(t)


class DGenerater(Generater):
    def __init__(self, env, generaterId, mean, classId=None):
        super().__init__(env, generaterId, classId)
        self._mean = mean

    def _duration(self):
        self._timeList.append(self._mean)
        yield self._env.timeout(self._mean)


class GGenerater(Generater):
    def __init__(self, env, generaterId, mean, classId=None):
        super().__init__(env, generaterId, classId)
        self._mean = mean

    def _duration(self):
        t = round(rd.random()*2*self._mean, 3)
        self._timeList.append(t)
        yield self._env.timeout(t)


if __name__ == '__main__':
    import myQueue as q
    import simpy
    env = simpy.Environment()
    g1 = MGenerater(env, 'g1', 10, 0)
    g2 = MGenerater(env, 'g2', 10, 1)
    q1 = q.MFQueue(env, 'q1', 3)
    q1.assignClass(1)
    q2 = q.DPQueue(env, 'q2', 3)
    g1.nextQueue = q1
    g2.nextQueue = q1
    q1.nextQueue = q2
    env.run(10000)
