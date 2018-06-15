#!/usr/bin/python
# coding: UTF-8
import simpy, random, numpy as np
import math
import collections as co
import csv
from datetime import datetime
import time
import threading as th


class Env():
    def __init__(self):
        self.env = simpy.Environment()
        random.seed()
        self.queue = []
        self.intime = []
        self.task1 = []
        self.end1 = []
        self.come = []
        self.total = []

    def arrive(self):
        name = 0
        self.env.process(self.into_queue())
        while True:
            yield self.env.timeout(random.expovariate(1.0/5))
            self.queue.append(self.env.now)
            self.task1.append(random.normalvariate(3,1)*100)

    def into_queue(self):
        stack = 0
        while True:
            yield self.env.timeout(0.01)
            if len(self.queue) == 0:
                continue
            work = 1
            j = stack
            self.task1[j] -= work
            if self.task1[j] <= 0:
                tm = self.queue[j]
                del self.queue[j]
                self.end1.append(self.env.now)
                self.intime.append(self.env.now - tm)
                del self.task1[j]
                j = j-1
            j += 1
            stack = j
            if stack == len(self.queue):
                stack = 0

    def run(self, times):
        self.env.process(self.arrive())
        startTime = time.time()
        self.env.run(times)
        endTime = time.time()
        lam = []
        for i in range(len(self.end1)-1):
          lam.append(self.end1[i+1]-self.end1[i])
        filename = "resultMN1PSout{}.csv".format(times)
        result = []
        for i in lam:
            result.append([1, i])
        print(endTime-startTime)
        print(np.average(lam))
        print('total = %d clients, W1 = %.2f' % (len(self.intime), np.average(self.intime)))
        with open(filename, "a") as f:
            writer = csv.writer(f,lineterminator="\n")
            writer.writerows(result)

if __name__ == '__main__':
    start = time.time()
    one = Env()
    two = Env()
    thread_1 = th.Thread(one.run(1000000))
    thread_2 = th.Thread(two.run(1000000))
    end = time.time()
    print(start-end)
