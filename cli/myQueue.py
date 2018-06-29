#!/usr/bin/python3
# coding: UTF-8
import random as rd
import numpy as np
import simpy
from abc import ABCMeta, abstractmethod
import sys


class Queue(metaclass=ABCMeta):
    def __init__(self, env, queueId, mean):
        self._env = env
        self._action = env.process(self.run())
        self._id = queueId
        self._nextQueue = None
        self._taskList = []
        self._executionTime = []
        self._mean = mean
        self._classList = [0]
        self._arrive = self._env.event()
        self._printAction = env.process(self.executionTime())

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

    def assignClass(self, className):
        self._classList.append(self._env.getClassList()[className])

    def _checkClass(self, classId):
        return classId in self._classList

    def executionTime(self):
        while True:
            yield self._env.timeout(1)
            if len(self._executionTime) == 0:
                ave = 0
            else:
                ave = np.average(self._executionTime)
            text = ' ' + self._id + (':%.3f' % ave)
            sys.stdout.write(text)
            sys.stdout.flush()

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
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)

    def addTask(self, task):
        if self._checkClass(task.classId):
            task.addQueueArrivedTime(self._id, self._env.now)
            self._taskList.append(task)
            self._arrive.succeed()
            self._arrive = self._env.event()

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
            self.executionTime()
            if self._nextQueue is not None:
                self._nextQueue.addTask(end)


class MFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mu = 1.0/mean

    def _work(self):
        yield self._env.timeout(rd.expovariate(self._mu))


class DFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mean = mean
        self._arrive = self._env.event()

    def _work(self):
        yield self._env.timeout(self._mean)


class PSQueue(Queue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._clock = 1000
        self._stack = 0

    def addTask(self, task):
        if self._checkClass(task.classId):
            task.addQueueArrivedTime(self._id, self._env.now)
            task.workload = self._work()
            self._taskList.append(task)
            self._arrive.succeed()
            self._arrive = self._env.event()

    def run(self):
        while True:
            if len(self._taskList) == 0:
                yield self._arrive
            yield self._env.timeout(round(1.0/self._clock,3))
            self._taskList[self._stack].workload -= 1
            if self._taskList[self._stack].workload <= 0:
                end = self._taskList[self._stack]
                del self._taskList[self._stack]
                end.addExitTime(self._id, self._env.now)
                time = self._env.now-end.getQueueArrivedTime(self._id)
                self._executionTime.append(time)
                self.executionTime()
                if self._nextQueue is not None:
                    self._nextQueue.addTask(end)
                self._stack -= 1
            self._stack += 1
            if self._stack == len(self._taskList):
                self._stack = 0


class MPQueue(PSQueue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mu = self._clock*mean

    def _work(self):
        return int(rd.expovariate(1.0/self._mu))


class DPQueue(PSQueue):
    def __init__(self, env, queueId, mean):
        super().__init__(env, queueId, mean)
        self._mean = self._clock*mean

    def _work(self):
        return int(self._mean)


if __name__ == '__main__':
    import myQueue as q
    env = simpy.Environment()
    g = q.DGenerater(env, 'g1', 5, 0)
    q1 = DPQueue(env, 'q1', 3)
    q2 = DPQueue(env, 'q2', 3)
    g.nextQueue = q1
    q1.nextQueue = q2
    env.run(10000)
    q1.executionTime()
    q2.executionTime()
