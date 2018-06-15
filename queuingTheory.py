#!/usr/bin/python3
# coding: UTF-8
import simpy, random as rd, numpy as np
import time
from abc import ABCMeta, abstractmethod

'''
class MyEnv
To extend the simpy.Environment class.
'''
class MyEnv(simpy.Environment):
    def __init__(self):
        super().__init__()

'''
class Arrival
To put new customers into the destination queue.
Arrival type:
    expovariate     "exp"
    deterministic   "det"
'''
class Arrival():
    def __init__(self, env): #type: env:MyEnv
        self._env = env
        self._mean = 0
        self._arrival = ''

# getter and setter of distribution type
    @property
    def expovariate(self):
        return self._mean if self._arrival is "exp" else None

    @expovariate.setter
    def expovariate(self, mean):
        self._arrival = "exp"
        self._mean = mean

    @property
    def deterministic(self):
        return self._mean if self._arrival is "det" else None

    @deterministic.setter
    def deterministic(self, interval):
        self._arrival = "det"
        self._mean = interval

    @property
    def arrivalType(self):
        return self._arrival

# getter and setter of nextQueue
    @property
    def nextQueue(self):
        return self._nextQueue

    @nextQueue.setter
    def nextQueue(self, nextQueue):
        self._nextQueue = nextQueue

    def _createTask(self):
        # TODO more complex task create method
        task = {
           'classType':0,
           'workload':0,
           'queueName':[],
           'queueArrivedTime':[],
           'exitTime':[]
           }
        return task

    def run(self):
        if self._arrival is "exp":
            while True:
                yield self._env.timeout(rd.expovariate(1.0/self._mean))
                self._nextQueue.addQueue(self._createTask())
        elif self._arrival is "det":
            while True:
                yield self._env.timeout(self._mean)
                self._nextQueue.addQueue(self._createTask())

'''
abstract class Queue
this class is super class of each queue class
Working time type:
    expovariate     "exp"
    deterministic   "det"
'''
class Queue(metaclass=ABCMeta):
    def __init__(self, env, queueId): #type: env:MyEnv
        self._env = env
        self._queue = []
        self._nextQueue = None
        self._id = queueId
        self._mean = 0
        self._work = ''

# getter and setter of queue id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, queueId):
        self._id = queueId

# getter and setter of nextQueue
    @property
    def nextQueue(self):
        return self._nextQueue

    @nextQueue.setter
    def nextQueue(self, nextQueue):
        self._nextQueue = nextQueue

# getter of queue
    @property
    def queue(self):
        return self._queue

# getter and setter of Working time type
    @property
    def expovariate(self):
        return self._mean if self._work is "exp" else None

    @expovariate.setter
    def expovariate(self, mean):
        self._work = "exp"
        self._mean = mean

    @property
    def deterministic(self):
        return self._mean if self._work is "det" else None

    @deterministic.setter
    def deterministic(self, interval):
        self._work = "det"
        self._mean = interval

    @property
    def workType(self):
        return self._work

# abstractmethods
    @abstractmethod
    def addQueue():
        '''
        task = {
            classType:,
            workload:,
            queueName:[...],
            queueArrivedTime:[...],
            exitTime:[...]
            }
        '''
        pass

    @abstractmethod
    def run(self):
        pass

'''
G/G/1-PS queue
Arrival of customers is depending of Arrival class or prev queue.
Working time type:
    expovariate     "exp"
    deterministic   "det"
'''
class PsQueue(Queue):
    def __init__(self, env, queueId, execTime):
        super().__init__(env, queueId)
        self._stack = 0
        self._execTime = execTime

    def addQueue(self, task):
        newTask = task
        if self._work is 'exp':
            newTask['workload'] = \
                int(rd.expovariate(1.0/self._mean)*(1.0/self._execTime))
        elif self._work is 'det':
            newTask['workload'] = \
                int(self._mean*(1.0/self._execTime))
        newTask['queueName'].append(self._id)
        newTask['queueArrivedTime'].append(self._env.now)
        self._queue.append(newTask)

    def run(self):
        while True:
            yield self._env.timeout(self._execTime)
            if len(self._queue) == 0:
                continue
            (self.queue[self._stack])['workload'] -= 1
            if (self._queue[self._stack])['workload'] <= 0:
                endTask = self._queue[self._stack]
                del self._queue[self._stack]
                endTask['exitTime'].append(self._env.now)
                if self._nextQueue is not None:
                    self._nextQueue.addQueue(endTask)
                # if there are customer classes, please add the branches
                self._stack -= 1
            self._stack += 1
            if self._stack == len(self._queue):
                self._stack = 0

class EndOfNet(object):
    def __init__(self):
        self._endTaskList = []

    @property
    def queue(self):
        return self._endTaskList

    def addQueue(self, endTask):
        self._endTaskList.append(endTask)

if __name__ == '__main__':
    env = MyEnv()
    arr = Arrival(env)
    q = PsQueue(env, 'q1', 0.01)
    q.expovariate = 3
    end = EndOfNet()
    arr.expovariate = 5
    arr.nextQueue = q
    q.nextQueue = end
    env.process(arr.run())
    env.process(q.run())
    env.run(1000000)
    workTime = []
    for i in end.queue:
        workTime.append(i['exitTime'][0]-i['queueArrivedTime'][0])
    print('%s = %.3f' % (end.queue[0]['queueName'][0],np.average(workTime)))
