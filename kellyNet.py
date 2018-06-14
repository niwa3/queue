#!/usr/bin/python
# coding: UTF-8
import simpy, random, numpy as np
import time
#import csv
#import pdb

__doc__ = """{f}
Usage:
    {f} [-e | --expovariate <mu>] [-d | --deterministic <nmu>]
    {f} -h | --help

Options:
    -e --expovariate         use expovariate (default)
    -d --deterministic       deterministic
    -h --help                Show this screen and exit.
""".format(f=__file__)

from docopt import docopt

class Env():
    def __init__(self):
        self.env = simpy.Environment()
        random.seed()
        self.queue1 = []
        self.queue2 = []
        self.queue3 = []
        self.end1 = []
        self.end2 = []
        self.total = []
        self.args = docopt(__doc__)

#first class of customer
    def arrive1(self):
        while True:
            yield self.env.timeout(random.expovariate(1.0/10))
            '''
            task = [
                0: class type,
                1: arrived time,
                2: workload 1,
                3: workload 2,
                4: workload 3,
                5: exit time 1,
                6: exit time 2,
                7: exit time 3]
            '''
            if self.args["--deterministic"]:
                task = [
                        1,
                        self.env.now,
                        int(self.args["<nmu>"])*100,
                        int(self.args["<nmu>"])*100,
                        int(self.args["<nmu>"])*100
                        ]
            elif self.args["--expovariate"]:
                task = [
                        1,
                        self.env.now,
                        int(random.expovariate(1.0/int(self.args["<mu>"]))*100),
                        int(random.expovariate(1.0/int(self.args["<mu>"]))*100),
                        int(random.expovariate(1.0/int(self.args["<mu>"]))*100)
                        ] 
            else:
                task = [
                        1,
                        self.env.now,
                        int(random.expovariate(1.0/3)*100),
                        int(random.expovariate(1.0/3)*100),
                        int(random.expovariate(1.0/3)*100)
                        ]
            self.queue1.append(task)

##second class of customer
    def arrive2(self):
        while True:
            yield self.env.timeout(random.expovariate(1.0/8))
            '''
            task = [
                0: class type,
                1: arrived time,
                2: workload 1,
                3: workload 2,
                4: workload 3,
                5: exit time 1,
                6: exit time 2,
                7: exit time 3]
            '''
            if self.args["--expovariate"]:
                task = [
                        2,
                        self.env.now,
                        int(self.args["<mu>"])*100,
                        int(self.args["<mu>"])*100,
                        int(self.args["<mu>"])*100
                        ]
            elif self.args["--deterministic"]:
                task = [
                        2,
                        self.env.now,
                        int(random.expovariate(1.0/int(self.args["<nmu>"]))*100),
                        int(random.expovariate(1.0/int(self.args["<nmu>"]))*100),
                        int(random.expovariate(1.0/int(self.args["<nmu>"]))*100)
                        ] 
            else:
                task = [
                        2,
                        self.env.now,
                        int(random.expovariate(1.0/3)*100),
                        int(random.expovariate(1.0/3)*100),
                        int(random.expovariate(1.0/3)*100)
                        ]
            self.queue1.append(task)

    def into_queue1(self):
        stack = 0
        while True:
            yield self.env.timeout(0.01)
            if len(self.queue1) == 0:
                continue
            work = 1
            j = stack
            (self.queue1[j])[2] -= work
            if (self.queue1[j])[2] <= 0:
                tm = self.queue1[j]
                del self.queue1[j]
                tm.append(self.env.now)
                if tm[0] == 1:
                    self.queue2.append(tm)
                else:
                    self.queue3.append(tm)
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
            (self.queue2[j])[3] -= work
            if (self.queue2[j])[3] <= 0:
                tm = self.queue2[j]
                del self.queue2[j]
                tm.append(self.env.now)
                self.queue3.append(tm)
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
            (self.queue3[j][4]) -= work
            if (self.queue3[j][4]) <= 0:
                tm = self.queue3[j]
                del self.queue3[j]
                tm.append(self.env.now)
                if tm[0] == 1:
                    self.end1.append(tm)
                else:
                    self.end2.append(tm)
                j = j-1
            j += 1
            stack3 = j
            if stack3 == len(self.queue3):
                stack3 = 0

    def run(self, times):
        self.env.process(self.arrive1())
        self.env.process(self.arrive2())
        self.env.process(self.into_queue1())
        self.env.process(self.into_queue2())
        self.env.process(self.into_queue3())
        startTime = time.time()
        self.env.run(times)
        endTime = time.time()
        lam1_1 = []
        lam1_2 = []
        lam1_3 = []
        for i in range(len(self.end1)-1):
          lam1_1.append(self.end1[i+1][1]-self.end1[i][1])
          lam1_2.append(self.end1[i+1][5]-self.end1[i][5])
          lam1_3.append(self.end1[i+1][6]-self.end1[i][6])
        lam2_1 = []
        #lam2_2 = []
        lam2_3 = []
        for i in range(len(self.end2)-1):
          lam2_1.append(self.end2[i+1][1]-self.end2[i][1])
          lam2_3.append(self.end2[i+1][5]-self.end2[i][5])
          #lam2_3.append(self.end2[i+1][6]-self.end2[i][6])
        intime1_1 = []
        intime1_2 = []
        intime1_3 = []
        total1 = []
        for task in self.end1:
          intime1_1.append(task[5]-task[1])
          intime1_2.append(task[6]-task[5])
          intime1_3.append(task[7]-task[6])
          total1.append(task[7]-task[1])
        intime2_1 = []
        #intime2_2 = []
        intime2_3 = []
        total2 = []
        for task in self.end2:
          intime2_1.append(task[5]-task[1])
          intime2_3.append(task[6]-task[5])
          #intime2_3.append(task[7]-task[6])
          #total2.append(task[7]-task[1])
          total2.append(task[6]-task[1])
        print("simulattion time = %.3f" % (endTime-startTime))
        print("total time 1 = %.3f" % (np.average(total1)))
        print("total time 2 = %.3f" % (np.average(total2)))
        print("arrival rate 1: %.3f, %.3f, %.3f" % (np.average(lam1_1), np.average(lam1_2), np.average(lam1_3)))
        #print("arrival rate 1: %.3f, %.3f, %.3f" % (np.average(lam2_1), np.average(lam2_2), np.average(lam2_3)))
        print("arrival rate 1: %.3f, %.3f" % (np.average(lam2_1), np.average(lam2_3)))
        print('class1: total = %d clients, W1 = %.2f, W2 = %.2f, W3 = %.2f' % (len(intime1_1), np.average(intime1_1), np.average(intime1_2), np.average(intime1_3)))
        #print('class2: total = %d clients, W1 = %.2f, W2 = %.2f, W3 = %.2f' % (len(intime2_1), np.average(intime2_1), np.average(intime2_2), np.average(intime2_3)))
        print('class2: total = %d clients, W1 = %.2f, W3 = %.2f' % (len(intime2_1), np.average(intime2_1), np.average(intime2_3)))
        #filename = "resultMD1{}.csv".format(times)
        #with open(filename, "a") as f:
        #    writer = csv.writer(f,lineterminator="\n")
        #    result = [np.average(intime1_1), np.average(intime1_2), np.average(intime1_3), np.average(intime2_1), np.average(intime2_2), np.average(intime2_3)]
        #    writer.writerow(result)

if __name__ == '__main__':
    one = Env()
    one.run(1000000)
