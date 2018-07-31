#!/usr/bin/python3
# coding: UTF-8

import math
import numpy as np


class QueueCalculator(object):
    def _wq(self, c, arrivalDuration, serviceDuration):
        q = serviceDuration/arrivalDuration

        def func(k): return ((c*q)**k)/math.factorial(k)
        w = ((c*q)**c/(math.factorial(c)*(1-q))) * \
            (1/(np.sum([func(i) for i in np.arange(c)]) +
                (c*q)**c/(math.factorial(c) * (1-q)))) / \
            ((1-q)*c/serviceDuration)
        return w

    def mmc(self, c, arrivalDuration, serviceDuration):
        w = self._wq(c, arrivalDuration, serviceDuration)+serviceDuration
        print('m/m/%d: W(%.3f, %.3f) = %.10f' %
              (c, arrivalDuration, serviceDuration, w))
        return w

    def mgc(self, c, arrivalDuration, serviceDuration, var):
        w = self._wq(c, arrivalDuration, serviceDuration) * \
            (1+var/(serviceDuration**2))/2+serviceDuration
        print('m/g/%d: W(%.3f, %.3f, %.3f) = %.10f' %
              (c, arrivalDuration, serviceDuration, var, w))
        return w

    def ggc(self, c, arrivalDuration, arrivalVar, serviceDuration, serviceVar):
        q = serviceDuration/arrivalDuration
        w = (q/(1-q)) * serviceDuration * \
            (arrivalVar/(arrivalDuration**2)+serviceVar/(serviceDuration**2)) / \
            2 + serviceDuration
        print('g/g/%d: W(%.3f, %.3f, %.3f, %.3f) = %.10f' %
              (c, arrivalDuration, arrivalVar, serviceDuration, serviceVar, w))
        return w

    def ps(self, c, arrivalDuration, serviceDuration):
        q = serviceDuration/arrivalDuration
        w = q / (1-q) * arrivalDuration
        print('m/g/%d: W(%.3f, %.3f) = %.10f' %
              (c, arrivalDuration, serviceDuration, w))
        return w


if __name__ == '__main__':
    c = QueueCalculator()
    # c.ggc(1, 20.005, 239.688, 9.998, 33.324)
    # c.ps(1, 10.01, 8.96)
    c.mmc(1, 1/3, 1/5)
    c.mmc(1, 1/6, 1/8)
