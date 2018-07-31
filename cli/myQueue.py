# !/usr/bin/python3
# coding: UTF-8

import random as rd
import numpy as np
import numpy.random as nr
import simpy.resources.store as store
from abc import ABCMeta, abstractmethod
# import csv
import caluclator as cal
# import datetime as date


class Queue(metaclass=ABCMeta):
    def __init__(self, env, queueId, mean, num=1):
        self._env = env
        self._action = []
        for i in range(num):
            self._action.append(env.process(self.run()))
        self._id = queueId
        self._nextQueue = None
        self._store = store.Store(env)
        self._arrivalTime = []
        self._executionTime = []
        self._serviceTime = []
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
        ave = np.average(self._executionTime)  # waiting time
        var = np.var(self._executionTime)
        aveB = np.average(self._serviceTime)  # service time
        varB = np.var(self._serviceTime)
        ls = []
        for i in range(len(self._arrivalTime)-1):
            x = self._arrivalTime[i+1] - self._arrivalTime[i]
            ls.append(round(x, 4))
        aveIn = np.average(ls)  # input interval
        varIn = np.var(ls)
        '''
        with open('input{0:%d%H}.csv'.format(date.datetime.now()), 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            ls = [self._id, ]+self._arrivalTime
            writer.writerow(ls)
        '''
        text = ' (' + self._id + ') '
        text += 'E(w):%.3f V(w):%.3f E(b):%.3f V(b):%.3f E(i):%.3f V(i):%.3f' \
                % (ave, var, aveB, varB, aveIn, varIn)
        print(text)
        c = cal.QueueCalculator()
        # c.ggc(1, aveIn, varIn, aveB, varB)
        c.ps(1, aveIn, aveB)

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
            self._arrivalTime.append(self._env.now)
            store.StorePut(self._store, task)
        else:
            self._func(task)

    def run(self):
        if self._nextQueue is not None:
            self._func = (lambda x: self._nextQueue.addTask(x))
        else:
            self._func = (lambda x: self._env.exitTask(x))
        while True:
            end = yield store.StoreGet(self._store)
            yield self._env.process(self._work())
            end.addExitTime(self._id, self._env.now)
            time = self._env.now-end.getQueueArrivedTime(self._id)
            self._executionTime.append(time)
            self._func(end)


class MFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mu = 1.0/mean

    def _work(self):
        t = round(rd.expovariate(self._mu), 3)
        self._serviceTime.append(t)
        yield self._env.timeout(t)


class DFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = mean

    def _work(self):
        t = self._mean
        self._serviceTime.append(t)
        yield self._env.timeout(self._mean)


class GFQueue(FCFSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = mean

    def _work(self):
        # t = rd.random()*self._mean*2
        t = abs(nr.normal(self._mean, 10))
        self._serviceTime.append(t)
        yield self._env.timeout(t)


class PSQueue(Queue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._clock = 1000
        self._round = 3
        # self._timeout = np.round(1.0/self._clock, self._round)
        self._timeout = 1

    def addTask(self, task):
        if self._checkClass(task.classId):
            task.addQueueArrivedTime(self._id, self._env.now)
            task.workload = self._work()
            self._arrivalTime.append(self._env.now)
            store.StorePut(self._store, task)
        else:
            self._func(task)

    def run(self):
        if self._nextQueue is not None:
            self._func = (lambda x: self._nextQueue.addTask(x))
        else:
            self._func = (lambda x: self._env.exitTask(x))
        '''
        while True:
            task = yield store.StoreGet(self._store)
            yield self._env.timeout(self._timeout)
            task.workload -= 1
            if task.workload <= 0:
                task.addExitTime(self._id, self._env.now)
                self._executionTime.append(
                    self._env.now-task.getQueueArrivedTime(self._id))
                self._func(task)
            else:
                store.StorePut(self._store, task)
        '''
        while True:
            yield self._env.timeout(self._timeout)
            queueLen = len(self._store.items)
            if queueLen == 0:
                continue
            work = self._clock/(queueLen*3)
            for i in range(queueLen):
                task = yield store.StoreGet(self._store)
                task.workload -= work
                if task.workload <= 0:
                    task.addExitTime(self._id, self._env.now)
                    self._executionTime.append(
                        self._env.now-task.getQueueArrivedTime(self._id))
                    self._func(task)
                    if len(self._store.items) == 0:
                        break
                else:
                    store.StorePut(self._store, task)
        '''
        あー，yieldの扱いが上手くいってないせいで，細かく区切ることができん
        '''


class MPQueue(PSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mu = mean

    def _work(self):
        t = rd.expovariate(1.0/self._mu)
        self._serviceTime.append(t)
        return int(t*self._clock)


class DPQueue(PSQueue):
    def __init__(self, env, queueId, mean, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = self._clock*mean

    def _work(self):
        t = self._mean
        self._serviceTime.append(t)
        return int(self._mean)


class GPQueue(PSQueue):
    def __init__(self, env, queueId, mean, var, num=1):
        super().__init__(env, queueId, mean, num)
        self._mean = mean
        self._var = var

    def _work(self):
        t = abs(nr.normal(self._mean, self._var))
        self._serviceTime.append(t)
        return int(t*self._clock)
