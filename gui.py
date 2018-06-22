#!/usr/bin python3
# -*- coding: utf-8 -*-

import wx
import queuingTheory as qt

class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)
        self._f = True
        self._x = 0
        self._y = 0

    def init_ui(self, env):
        self.env = env
        self.env.window = self
        self.SetTitle('タイトル')
        self.SetSize((800, 600))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(1)
        w, h = self.GetClientSize()
        self.mainPanel = wx.Panel(self, size=(w, h))
        self.mainPanel.SetBackgroundColour('white')
        self.panel1 = wx.Panel(self.mainPanel)
        self.panel2 = wx.Panel(self.mainPanel)
        self.panel3 = wx.Panel(self.mainPanel)
        layout = wx.GridSizer(rows=3, cols=3, gap=(0,0))
        layout.Add(self.panel1, flag=wx.GROW)
        layout.Add(self.panel2, flag=wx.GROW)
        layout.Add(self.panel3, flag=wx.GROW)
        self.mainPanel.SetSizer(layout)

        self.Show()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self._buffer)

    def OnSize(self, evt):
        w, h = self.GetClientSize()
        self._buffer = wx.EmptyBitmap(w,h)
        self.InitBuffer()
        self.DrawToBuffer()

    def OnTimer(self, evt):
        self.env.step()

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
    q1 = env.createPsQueue('q1', 0.01)
    q2 = env.createPsQueue('q2', 0.01)
    q3 = env.createFcfsQueue('q3')

    arr1.expovariate = 10
    arr2.expovariate = 10
    q1.expovariate = 3
    q2.expovariate = 3
    q3.expovariate = 3

    end = env.createEnd()

    env.createNet(arr1, q1)
    env.createNet(arr2, q1)
    env.createNet(q1, q2)
    env.createNet(q2, q3)
    env.createNet(q3, end)

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
