#!/usr/bin python3
# -*- coding: utf-8 -*-

import wx
import queuingTheoryGui as qt

class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)
        self._f = True
        self._x = 0
        self._y = 0

    def init_ui(self, env):
        self.env = env
        self.SetTitle('タイトル')
        self.SetSize((800, 600))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(1)
        self.Show()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)

    def OnSize(self, evt):
        w, h = self.GetClientSize()
        self._buffer = wx.EmptyBitmap(w,h)
        self.InitBuffer()
        self.DrawToBuffer()

    def OnTimer(self, evt):
        self.InitBuffer()
        self._dc.Clear()
        self.env.step()
        self.env.draw(self._dc)

    def InitBuffer(self):
        self._dc = wx.BufferedDC(wx.ClientDC(self), self._buffer)
        brush = wx.Brush('white')
        self._dc.SetBackground(brush)
        self._dc.SetPen(wx.Pen('blue',3))

    def DrawToBuffer(self):
        self._dc.Clear()
        w, h = self._dc.GetSize()

if __name__ == '__main__':
    print('starting...')
    env = qt.MyEnv()

    env.createClassType('customer1')
    env.createClassType('customer2')

    arr1 = env.createArrival('a1', 'customer1')
    arr1.x = 50
    arr1.y = 50
    arr2 = env.createArrival('a2', 'customer2')
    arr2.x = 50
    arr2.y = 200
    q1 = env.createPsQueue('q1')
    q1.x = 150
    q1.y = 125
    q2 = env.createPsQueue('q2')
    q2.x = 250
    q2.y = 125
    q3 = env.createPsQueue('q3')
    q3.x = 350
    q3.y = 125

    arr1.expovariate = 0.1
    arr2.expovariate = 0.1
    q1.expovariate = 0.03
    q2.expovariate = 0.03
    q3.expovariate = 0.03

    end = env.createEnd()
    end.x = 450
    end.y = 125

    env.createNet(arr1, q1, 1)
    env.createNet(arr2, q1, 1)
    env.createNet(q1, q2, 1)
    env.createNet(q2, q3, 1)
    env.createNet(q3, end, 1)

    env.assineClassToQueue('customer1', q1)
    env.assineClassToQueue('customer1', q2)
    env.assineClassToQueue('customer1', q3)

    env.assineClassToQueue('customer2', q1)
    env.assineClassToQueue('customer2', q3)

    env.process()

    app = wx.App()
    myApp = MyApp(None)
    myApp.init_ui(env)
    app.MainLoop()
