import simpy, random, numpy as np
#import matplotlib.pyplot as plt
import math
#import matplotlib.animation as animation
import collections as co

random.seed()
env = simpy.Environment()

queue, intime = [], []
queue2, intime2 = [], []

task1, task2 = [], []


end1 = []
end2 = []
come, total = [], []


#ims = []
#fig = plt.figure()

def arrive():
    global cusName
    global queue
    global task1
    name = 0
    env.process(into_queue())
    env.process(into_queue2())
    while True:
        yield env.timeout(random.expovariate(1.0/5))
        queue.append(env.now)
        task1.append((int)(random.expovariate(1.0/3)*100))

def into_queue():
    global queue
    global end1
    global task1
    global queue2
    global task2
    stack = 0
    while True:
        yield env.timeout(0.01)
        if len(queue) == 0:
            continue
        work = 1
        if len(task1)==0:
            break
        j = stack
        task1[j] -= work
        #print(env.now, task1)
        if task1[j] <= 0:
            tm = queue[j]
            del queue[j]
            end1.append(env.now)
            intime.append(env.now - tm)
            del task1[j]
            queue2.append(env.now)
            task2.append((int)(random.expovariate(1.0/3)*100))
            j = j-1
        j += 1
        stack = j
        if stack == len(queue):
            stack = 0

def into_queue2():
    global queue2
    global end2
    global task2
    stack2= 0
    while True:
        yield env.timeout(0.01)
        if len(queue2) == 0:
            continue
        work = 1
        if len(task2)==0:
            break
        j = stack2
        task2[j] -= work
        #print(env.now, task2)
        if task2[j] <= 0:
            tm = queue2[j]
            del queue2[j]
            end2.append(env.now)
            intime2.append(env.now - tm)
            del task2[j]
            j = j-1
        j += 1
        if stack2 == len(queue2):
            stack2 = 0

env.process(arrive())
env.run(100000)

lam = []
for i in range(len(end1)-1):
  lam.append(end1[i+1]-end1[i])
    
print(np.average(lam))

#print('total = %d clients, W1 = %.2f, W2 = %.2f, Wtot = %.2f' % (len(intime), np.average(intime), np.average(intime2), np.average(total)))
#print('total = %d clients, W1 = %.2f' % (len(intime), np.average(intime)))
print('total = %d clients, W1 = %.2f, W2 = %.2f' % (len(intime), np.average(intime), np.average(intime2)))
#ani = animation.ArtistAnimation(fig, ims, interval=10)
