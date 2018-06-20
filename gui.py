#!/usr/bin python3
# -*- coding: utf-8 -*-

import wx

class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)
        self._f = True
        self.init_ui()
        self._x = 0
        self._y = 0

    def init_ui(self):
        self.SetTitle('タイトル')
        self.SetSize((800, 600))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer = wx.Timer(self)
        self.timer.Start(10)
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
        self.DrawBall()

    def InitBuffer(self):
        self._dc = wx.BufferedDC(wx.ClientDC(self), self._buffer)
        brush = wx.Brush('white')
        self._dc.SetBackground(brush)
        self._dc.SetPen(wx.Pen('blue',3))

    def DrawToBuffer(self):
        self._dc.Clear()
        w, h = self._dc.GetSize()
        self._dc.DrawCircle(w/2,h/2,100)

    def DrawBall(self):
        self._dc.Clear()
        self._dc.DrawCircle(self._x, self._y, 100)
        self._x += 1
        self._y += 1

if __name__ == '__main__':
    app = wx.App()
    MyApp(None)
    app.MainLoop()
