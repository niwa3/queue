#!/usr/bin/python3
# coding: UTF-8
import random as rd
import numpy as np
import simpy.resources.store as store
from abc import ABCMeta, abstractmethod

class Queue(metaclass=ABCMeta):
    def __init__(self, env, queueId, mean, num=1):
        self._env = env
        self._action = []
        for i in range(num):
            self._action.append(env.process(self.run()))
        self._id = queueId
        self._nextQueue = None
        self._store = store.Store(env)
        self._executionTime = []
        self._mean = mean
        self._classList = [0]

    @property
    def id(self):
        return self._queueId

    @property
    def nextQueue(self):
        return self._nextQueue

    @nextQueue.setter
    def nextQueue(self, queue):
        self._nextQueue = queue

    @property
    def store(self):
        return self._store

    def assignClass(self, className):
        self._classList.append(self._env.classNameToId(className))

    def _checkClass(self, classId):
        return classId in self._classList

    def printResult(self):
        ave = np.average(self._executionTime)
        text = ' (' + self._id + ') mean:%.3f'%ave
        print(text)

    @abstractmethod
    def addTask(self, task):
        pass

    @abstractmethod
    def _work(self):
        pass

    @abstractmethod
    def run(self):
        pass


class FCFSQueue(Queue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)

    def addTask(self, task):
        if self._checkClass(task.classId):
            task.addQueueArrivedTime(self._id, self._env.now)
            store.StorePut(self._store, task)
        else:
            if self._nextQueue is not None:
                self._nextQueue.addTask(task)
            else:
                self._env.exitTask(task)

    def run(self):
        while True:
            end = yield store.StoreGet(self._store)
            yield self._env.process(self._work())
            end.addExitTime(self._id, self._env.now)
            time = self._env.now-end.getQueueArrivedTime(self._id)
            self._executionTime.append(time)
            if self._nextQueue is not None:
                self._nextQueue.addTask(end)
            else:
                self._env.exitTask(end)


class MFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mu = 1.0/mean

    def _work(self):
        yield self._env.timeout(round(rd.expovariate(self._mu),3))


class DFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = mean

    def _work(self):
        yield self._env.timeout(self._mean)


class GFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = mean

    def _work(self):
        yield self._env.timeout(rd.random()*self._mean*2)


class PSQueue(Queue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._clock = 1000

    def addTask(self, task):
        if self._checkClass(task.classId):
            task.addQueueArrivedTime(self._id, self._env.now)
            task.workload = self._work()
        else:
            if self._nextQueue is not None:
                self._nextQueue.addTask(task)
            else:
                self._env.exitTask(task)
            store.StorePut(self._store, task)

    def run(self):
        while True:
            task = yield store.StoreGet(self._store)
            yield self._env.timeout(round(1.0/self._clock,3))
            task.workload -= 1
            if task.workload <= 0:
                task.addExitTime(self._id, self._env.now)
                time = self._env.now-task.getQueueArrivedTime(self._id)
                self._executionTime.append(time)
                if self._nextQueue is not None:
                    self._nextQueue.addTask(task)
                else:
                    self._env.exitTask(task)
            else:
                store.StorePut(self._store, task)


class MPQueue(PSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mu = self._clock*mean

    def _work(self):
        t = int(rd.expovariate(1.0/self._mu))
        return t


class DPQueue(PSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = self._clock*mean

    def _work(self):
        return int(self._mean)


class GPQueue(PSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = self._clock*mean

    def _work(self):
        t = rd.random()*self._mean*2
        return int(t)
