#!/usr/bin/python
# coding: UTF-8

'''
This programe is aming to simulate the m/d/1-ps jackson network.
customers arrive at queue1 with the poisson of 1/5 rate.
And then, the customer finished work at queue1 arrives at queue2.
Finaly, customers exite this system from queue3.
'''

import simpy, random, numpy as np
import csv
import time

class Env():
    def __init__(self):
        self.env = simpy.Environment()
        random.seed()
        self.queue1 = []
        self.intime1 = []
        self.task1 = []
        self.end1 = []
        self.come1 = []
        self.queue2 = []
        self.intime2 = []
        self.task2 = []
        self.end2 = []
        self.come2 = []
        self.queue3 = []
        self.intime3 = []
        self.task3 = []
        self.end3 = []
        self.come3 = []
        self.total = []

    def arrive(self):
        self.env.process(self.into_queue1())
        self.env.process(self.into_queue2())
        self.env.process(self.into_queue3())
        while True:
            yield self.env.timeout(random.expovariate(1.0/5))
            self.come1.append(self.env.now)
            self.queue1.append(self.env.now)
            self.task1.append(3*100)

    def into_queue1(self):
        stack = 0
        while True:
            yield self.env.timeout(0.01)
            if len(self.queue1) == 0:
                continue
            work = 1
            j = stack
            self.task1[j] -= work
            if self.task1[j] <= 0:
                tm = self.queue1[j]
                del self.queue1[j]
                self.end1.append(self.env.now)
                self.intime1.append(self.env.now - tm)
                self.queue2.append(self.env.now)
                self.come2.append(self.come1[j])
                del self.task1[j]
                del self.come1[j]
                self.task2.append(3*100)
                j = j-1
            j += 1
            stack = j
            if stack == len(self.queue1):
                stack = 0

    def into_queue2(self):
        stack2= 0
        while True:
            yield self.env.timeout(0.01)
            if len(self.queue2) == 0:
                continue
            work = 1
            j = stack2
            self.task2[j] -= work
            if self.task2[j] <= 0:
                tm = self.queue2[j]
                del self.queue2[j]
                self.end2.append(self.env.now)
                self.intime2.append(self.env.now - tm)
                self.queue3.append(self.env.now)
                self.come3.append(self.come2[j])
                del self.task2[j]
                del self.come2[j]
                self.task3.append(3*100)
                j = j-1
            j += 1
            stack2 = j
            if stack2 == len(self.queue2):
                stack2 = 0

    def into_queue3(self):
        stack3= 0
        while True:
            yield self.env.timeout(0.01)
            if len(self.queue3) == 0:
                continue
            work = 1
            j = stack3
            self.task3[j] -= work
            if self.task3[j] <= 0:
                tm = self.queue3[j]
                del self.queue3[j]
                self.end3.append(self.env.now)
                self.intime3.append(self.env.now - tm)
                self.total.append(self.env.now - self.come3[j])
                del self.task3[j]
                del self.come3[j]
                j = j-1
            j += 1
            stack3 = j
            if stack3 == len(self.queue3):
                stack3 = 0

    def run(self, times):
        self.env.process(self.arrive())
        startTime = time.time()
        self.env.run(times)
        endTime = time.time()
        lam = []
        lam2 = []
        lam3 = []
        for i in range(len(self.end1)-1):
          lam.append(self.end1[i+1]-self.end1[i])
        for i in range(len(self.end2)-1):
          lam2.append(self.end2[i+1]-self.end2[i])
        for i in range(len(self.end3)-1):
          lam3.append(self.end3[i+1]-self.end3[i])
        print("simulattion time = %.3f" % (endTime-startTime))
        print("total time = %.3f" % (np.average(self.total)))
        print("arrival rate 1: %.3f" % (np.average(lam)))
        print("arrival rate 2: %.3f" % (np.average(lam2)))
        print("arrival rate 3: %.3f" % (np.average(lam3)))
        print('total = %d clients, W1 = %.2f, W2 = %.2f, W3 = %.2f' % (len(self.intime1), np.average(self.intime1), np.average(self.intime2), np.average(self.intime3)))
        filename = "resultMD1{}.csv".format(times)
        with open(filename, "a") as f:
            writer = csv.writer(f,lineterminator="\n")
            result = [np.average(lam), np.average(self.intime1), np.average(self.intime2)]
            writer.writerow(result)
        #ani = animation.ArtistAnimation(fig, ims, interval=10)

if __name__ == '__main__':
    one = Env()
    one.run(100000)
