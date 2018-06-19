#!/usr/bin python3
# -*- coding: utf-8 -*-

import wx

class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)
        self._f = True
        self.init_ui()

    def init_ui(self):
        self.SetTitle('タイトル')
        #self.SetSize((400, 300))
        self.Show()
        self.display()

    def display(self):
        self._panel = wx.Panel(self, -1, pos=(10,10), size=(180,260))
        self._cdc = wx.ClientDC(self._panel)
        w, h = self._panel.GetSize()
        self._bmp = wx.Bitmap(w,h)
        self._bdc = wx.BufferedDC(self._cdc, self._bmp)
        self._bdc.SetPen(wx.Pen('red'))
        self._bdc.SetBrush(wx.Brush('red'))
        self._bdc.DrawCircle(50,50,10)
        self._cdc.DrawBitmap(self._bmp,0,0)

    def panelUi(self):
        self._panel_ui = wx.Panel(self, -1, pos=(50,50), size=(300,200))

    def label(self):
        self._label = wx.StaticText(self._panel_ui, -1, pos=(10, 10))
        self._label.SetLabel('Hello')
        self._f = False

    def button(self):
        btn = wx.Button(self._panel_ui, -1, 'copy', pos=(10,90))
        btn.Bind(wx.EVT_BUTTON, self.clicked)

    def box(self):
        self._box = wx.TextCtrl(self._panel_ui, -1, pos=(10,50))

    def clicked(self, event):
        text = self._box.GetValue()
        self._box.Clear()
        self._label.SetLabel(text)

if __name__ == '__main__':
    app = wx.App()
    MyApp(None)
    app.MainLoop()
