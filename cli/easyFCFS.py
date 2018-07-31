# !/usr/bin/python3
# coding: UTF-8
import random as rd
import simpy
import simpy.resources.store as st


class Customer():
    def __init__(self, env, store):
        self._env = env
        self._action = env.process(self.run())
        self._store = store

    def run(self):
        i = 0
        while True:
            yield self._env.timeout(rd.expovariate(1.0/5))
            print('At %.3f, customer %d arrives' % (self._env.now, i))
            st.StorePut(self._store, i)
            i += 1


class Queue():
    def __init__(self, env, store):
        self._env = env
        self._action = env.process(self.run())
        self._store = store

    def run(self):
        while True:
            i = yield st.StoreGet(self._store)
            print('At %.3f, service for customer %d start...' %
                  (self._env.now, i))
            yield self._env.timeout(rd.expovariate(1.0/3))
            print('At %.3f, service for customer %d end' % (self._env.now, i))


if __name__ == '__main__':
    env = simpy.Environment()
    store = st.Store(env)
    c = Customer(env, store)
    q = Queue(env, store)
    env.run(100)
