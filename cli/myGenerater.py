#!/usr/bin/python3
# coding: UTF-8
import random as rd
import myTask as t


class Generater(object):
    def __init__(self, env, classId=None):
        self._env = env
        self._action = env.process(self.run())
        self._nextQueue = None
        self._classId = classId

    @property
    def nextQueue(self):
        return self._nextQueue

    @nextQueue.setter
    def nextQueue(self, queue):
        self._nextQueue = queue

    def _createTask(self):
        task = t.Task(self._classId or 0)
        return task

    def run(self):
        while True:
            yield self._env.timeout(rd.expovariate(1.0/5))
            #yield self._env.timeout(5)
            self._nextQueue.addTask(self._createTask())


if __name__ == '__main__':
    import myQueue as q
    import simpy
    env = simpy.Environment()
    g = Generater(env)
    q = q.MFQueue(env, 'q1', 3)
    g.nextQueue = q
    env.run(1000)
    q.executionTime()
