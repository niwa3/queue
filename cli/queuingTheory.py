#!/usr/bin/python3
# coding: UTF-8
import simpy, random as rd, numpy as np
from abc import ABCMeta, abstractmethod

'''
class MyEnv
To extend the simpy.Environment class.
'''
class MyEnv(simpy.Environment):
    def __init__(self):
        super().__init__()
        self._arrivalList = []
        self._queueList = []
        self._netList = []
        self._class = CustomerClass()

    @property
    def arrivalList(self):
        return self._arrivalList

    @property
    def queuList(self):
        return self._queueList

    def createClassType(self, classId):
        self._class.createNewType(classId)

    def createArrival(self, arrivalId, classId = None):
        _arrival = Arrival(self, arrivalId)
        if classId is not None:
            _arrival.classType = self._class.idToIndex(classId)
        self._arrivalList.append(_arrival)
        return _arrival

# it is not recomended to use this func
    def addArrival(self, arrival):
        self._arrivalList.append(arrival)

    def createPsQueue(self, queueId):
        _queue = PsQueue(self, queueId)
        self._queueList.append(_queue)
        return _queue

    def createFcfsQueue(self, queueId):
        _queue = FcfsQueue(self, queueId)
        self._queueList.append(_queue)
        return _queue

# it is not recomended to use this func
    def addQueue(self, queue):
        self._queueList.append(queue)

# now, there is no commection delay
    def createNet(self, fromQueue, toQueue):
        fromQueue.nextQueue = toQueue

    def createEnd(self):
        self._end = EndOfNet()
        return self._end

    def assineClassToQueue(self, classId, toQueue):
        toQueue.addClass(self._class.idToIndex(classId))

    def process(self):
        for i in self._arrivalList:
            super().process(i.run())
        for i in self._queueList:
            super().process(i.run())

    def run(self, numOfLoop):
        self.process()
        super().run(numOfLoop)

class CustomerClass(object):
    def __init__(self):
        # [1, 2, ...]
        self._typeList = []
        # {'A':0, 'B':1, ...}
        self._idToIndex = {}
        self._nextIndex = 1

    @property
    def typeList(self):
        return self._typeList

    def createNewType(self, classId):
        self._idToIndex[classId] = self._nextIndex
        self._typeList.append(self._nextIndex)
        self._nextIndex += 1

    def idToIndex(self, classId):
        return self._idToIndex[classId]

class Customer(object):
    def __init__(self, classType):
        self._classType = classType
        self._workload = 0
        self._queueId = []
        self._queueArrivedTime = []
        self._exitTime = []

    @property
    def classType(self):
        return self._classType

    @classType.setter
    def classType(self, classType):
        self._classType = classType

    @property
    def workload(self):
        return self._workload

    @workload.setter
    def workload(self, workload):
        self._workload = workload

    def addQueueId(self, queueId):
        self._queueId.append(queueId)

    def getQueueId(self):
        return self._queueId

    def addQueueArrivedTime(self, time):
        self._queueArrivedTime.append(time)

    def getQueueArrivedTime(self):
        return self._queueArrivedTime

    def addExitTime(self, time):
        self._exitTime.append(time)

    def getExitTime(self):
        return self._exitTime

class Net(object):
    def __init__(self, fromQueue, toQueue):
        self._from = fromQueue
        self._to = toQueue
        self._taskList = []
        self._currentDelay = []
        self._delay = 0

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, delay):
        self._delay = delay

    def addQueue(self, task):
        self._taskList.append(task)
        self._currentDelay.append(self._delay)

    def run(self):
        while True:
            yield self._env.timeout(0.001)
            for i in range(len(self._currentDelay)):
                self._currentDelay[i] -= 1
                if self._currentDelay[i] == 0:
                    del self._currentDelay[i]
                    self._to.addQueue(self._taskList[i])
                    del self._taskList[i]
                    i -= 1


'''
class Arrival
To put new customers into the destination queue.
Arrival type:
    expovariate     "exp"
    deterministic   "det"
'''
class Arrival():
    def __init__(self, env, arrivalId): #type: env:MyEnv
        self._env = env
        self._mean = 0
        self._arrival = ''
        self._id = arrivalId
        self._classType = 0

# getter of id
    @property
    def id(self):
        return self._id

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

# getter and setter of classType
    @property
    def classType(self):
        return self._classType

    @classType.setter
    def classType(self, classType):
        self._classType = classType

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def _createTask(self):
        return Customer(self._classType)

    def run(self):
        if self._arrival is "exp":
            while True:
                yield self._env.timeout(round(rd.expovariate(1.0/self._mean), 3))
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
        self._classList = [0]

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

    @property
    def classList(self):
        return self._classList

    def addClass(self, classType):
        self._classList.append(classType)

    def _checkClass(self, classType):
        if classType not in self._classList:
            return False
        return True

# abstractmethods
    @abstractmethod
    def addQueue(self, task):
        '''
        class Customer()
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
    def __init__(self, env, queueId):
        super().__init__(env, queueId)
        self._stack = 0
        self._execTime = 0.001

    def addQueue(self, task):
        newTask = task
        if self._checkClass(newTask.classType) is False:
            self._nextQueue.addQueue(newTask)
        else:
            if self._work is 'exp':
                newTask.workload = \
                    int(rd.expovariate(1.0/self._mean)*(1.0/self._execTime))
            elif self._work is 'det':
                newTask.workload = \
                    int(self._mean*(1.0/self._execTime))
            newTask.addQueueId(self._id)
            newTask.addQueueArrivedTime(self._env.now)
            self._queue.append(newTask)

    def run(self):
        while True:
            yield self._env.timeout(self._execTime)
            if len(self._queue) == 0:
                continue
            self.queue[self._stack].workload -= 1
            if (self._queue[self._stack]).workload <= 0:
                endTask = self._queue[self._stack]
                del self._queue[self._stack]
                endTask.addExitTime(self._env.now)
                if self._nextQueue is not None:
                    self._nextQueue.addQueue(endTask)
                # if there are customer classes, please add the branches
                self._stack -= 1
            self._stack += 1
            if self._stack == len(self._queue):
                self._stack = 0

'''
G/G/1-FCFS
あー，これは微妙か？
タスクが来てから一定時間後に処理するんなら，
タスクが来てからカウントが始まらないといけない気もする
PSの方法を採用したほうが時間は少ないのか
'''
class FcfsQueue(Queue):
    def __init__(self, env, queueId):
        super().__init__(env, queueId)

    def addQueue(self, task):
        newTask = task
        if self._checkClass(newTask.classType) is False:
            self._nextQueue.addQueue(newTask)
        else:
            newTask.workload = 0
            newTask.addQueueId(self._id)
            newTask.addQueueArrivedTime(self._env.now)
            self._queue.append(newTask)

    def run(self):
        if self._work is 'exp':
            while True:
                yield self._env.timeout(rd.expovariate(1.0/self._mean))
                if len(self._queue) == 0:
                    continue
                endTask = self._queue[0]
                del self._queue[0]
                endTask.addExitTime(self._env.now)
                if self._nextQueue is not None:
                    self._nextQueue.addQueue(endTask)
        elif self._work is 'det':
            while True:
                yield self._env.timeout(self._mean)
                if len(self._queue) == 0:
                    continue
                endTask = self._queue[0]
                del self._queue[0]
                endTask.addExitTime(self._env.now)
                if self._nextQueue is not None:
                    self._nextQueue.addQueue(endTask)

class EndOfNet(object):
    def __init__(self):
        self._endTaskList = []

    @property
    def queue(self):
        return self._endTaskList

    def addQueue(self, endTask):
        self._endTaskList.append(endTask)

    def printResult(self):
        workTimes = {}
        for c in self._endTaskList:
            if c.classType not in workTimes.keys():
                workTimes[c.classType] = []
            workTimes[c.classType].append(c)
        for k in workTimes.keys():
            print(k)
            for q in range(len(workTimes[k][0].getQueueId())):
                workTimeList = []
                workTime = []
                for i in workTimes[k]:
                    workTime.append(i.getExitTime()[q]-i.getQueueArrivedTime()[q])
                workTimeList.append(workTime)
                print('%s = %.3f' %
                        (workTimes[k][0].getQueueId()[q],np.average(workTime))
                    )

if __name__ == '__main__':
    print('starting...')
    env = MyEnv()

    env.createClassType('customer1')
    env.createClassType('customer2')

    arr1 = env.createArrival('a1', 'customer1')
    arr2 = env.createArrival('a2', 'customer2')
    q1 = env.createPsQueue('q1')
    q2 = env.createPsQueue('q2')
    q3 = env.createFcfsQueue('q3')

    arr1.expovariate = 10
    arr2.expovariate = 10
    q1.expovariate = 3
    q2.expovariate = 3
    q3.expovariate = 3

    end = env.createEnd()

    env.createNet(arr1, q1)
    env.createNet(arr2, q1)
    env.createNet(q1, q2)
    env.createNet(q2, q3)
    env.createNet(q3, end)

    env.assineClassToQueue('customer1', q1)
    env.assineClassToQueue('customer1', q2)
    env.assineClassToQueue('customer1', q3)

    env.assineClassToQueue('customer2', q1)
    env.assineClassToQueue('customer2', q3)

    env.run(1000)

    end.printResult()
