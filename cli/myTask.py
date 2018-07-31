# !/usr/bin/python3
# coding: UTF-8


class Task(object):
    def __init__(self, classId):
        self._classId = classId
        self._workload = 0
        self._queueArrivedTime = {}
        self._exitTime = {}

    @property
    def classId(self):
        return self._classId

    @classId.setter
    def classId(self, classId):
        self._classId = classId

    @property
    def workload(self):
        return self._workload

    @workload.setter
    def workload(self, workload):
        self._workload = workload

    def getQueueIdList(self):
        return list(self._queueArrivedTime)

    def addQueueArrivedTime(self, queueId, time):
        self._queueArrivedTime[queueId] = time

    def getQueueArrivedTime(self, queueId):
        return self._queueArrivedTime[queueId]

    def getQueueArrivedTimeList(self):
        return self._queueArrivedTime

    def addExitTime(self, queueId, time):
        self._exitTime[queueId] = time

    def getExitTime(self, queueId):
        return self._exitTime[queueId]

    def getExitTimeList(self):
        return self._exitTime
