#!/usr/bin/python3
# coding: UTF-8
import random as rd
import numpy as np
import simpy
#import myTask as t
from abc import ABCMeta, abstractmethod


class Queue(metaclass=ABCMeta):
    def __init__(self, env, queueId, mean):
        self._env = env
        self._action = env.process(self.run())
        self._id = queueId
        self._nextQueue = None
        self._taskList = []
        self._executionTime = []
        self._mean = mean
        self._classList = []

    @property
    def action(self):
        return self._action

    @property
    def id(self):
        return self._queueId

    @property
    def nextQueue(self):
        return self._nextQueue

    @nextQueue.setter
    def nextQueue(self, queue):
        self._nextQueue = queue

    def addClass(self, classId):
        self._classList.append(classId)

    def _checkClass(self, classId):
        return classId in self._classList

    def executionTime(self):
        print('mean: %.3f' % np.average(self._executionTime))

    @abstractmethod
    def addTask(self, task):
        pass

    @abstractmethod
    def _work(self):
        pass

    @abstractmethod
    def run(self):
        pass


class MFQueue(Queue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mu = 1.0/mean
        self._arrive = self._env.event()

    def addTask(self, task):
        task.addQueueArrivedTime(self._id, self._env.now)
        self._taskList.append(task)
        self._arrive.succeed()
        self._arrive = self._env.event()

    def _work(self):
        yield self._env.timeout(rd.expovariate(self._mu))

    def run(self):
        while True:
            try:
                if len(self._taskList) == 0:
                    yield self._arrive
                yield self._env.process(self._work())
                end = self._taskList[0]
                del self._taskList[0]
                end.addExitTime(self._id, self._env.now)
                time = self._env.now-end.getQueueArrivedTime(self._id)
                self._executionTime.append(time)
                if self._nextQueue is not None:
                    self._nextQueue.addTask(end)
            except simpy.Interrupt:
                continue

class MPQueue(Queue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mu = 1000.0/mean

    def addTask(self, task):
        task.addQueueArrivedTime(self._id, self._env.now)
        task.workload = int(rd.expovariate(self._mu))
        self._taskList.append(task)


class DFQueue(Queue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mean = mean
        self._arrive = self._env.event()

    def addTask(self, task):
        task.addQueueArrivedTime(self._id, self._env.now)
        self._taskList.append(task)
        self._arrive.succeed()
        self._arrive = self._env.event()

    def _work(self):
        yield self._env.timeout(self._mean)

    def run(self):
        while True:
            if len(self._taskList) == 0:
                yield self._arrive
            yield self._env.process(self._work())
            end = self._taskList[0]
            del self._taskList[0]
            end.addExitTime(self._id, self._env.now)
            time = self._env.now-end.getQueueArrivedTime(self._id)
            self._executionTime.append(time)
            if self._nextQueue is not None:
                self._nextQueue.addTask(end)


if __name__ == '__main__':
    import myGenerater as g
    env = simpy.Environment()
    g = g.Generater(env)
    q = Queue(env)
    g.nextQueue = q
    env.run(1000)
    q.executionTime()
