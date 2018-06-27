#!/usr/bin/python3
# coding: UTF-8
import simpy 
import myQueue as q
import myGenerater as g

'''
class MyEnv
To extend the simpy.Environment class.
'''
class MyEnv(simpy.Environment):
    def __init__(self):
        super().__init__()

    def Generater(self):
        generater = g.Generater(self)
        return generater

    def Queue(self):
        queue = q.Queue(self)
        return queue
