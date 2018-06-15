#!/usr/bin python3
# -*- coding: utf-8 -*-

import wx

class MyApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(MyApp, self).__init__(*args, **kw)

        self.init_ui()

    def init_ui(self):
        self.SetTitle('タイトル')
        self.SetPosition((200, 100))
        self.SetSize((400, 300))
        self.Show()
        self.label()

    def display(self):
        panel_G = wx.Panel(self, -1, pos=(10,10), size=(180,260))
        panel_G.SetBackgroundColour((0,255,0))

        panel_B = wx.Panel(self, -1)
        panel_B.SetBackgroundColour((0,0,255))
        panel_B.SetPosition((210,10))
        panel_B.SetSize((180,260))

    def label(self):
        panel_ui = wx.Panel(self, -1, pos=(50,50), size=(300,200))
        panel_ui.SetBackgroundColour((0,255,0))
        label_jp = wx.StaticText(panel_ui, -1, 'こんにちは', pos = (10,10))
        label_en = wx.StaticText(panel_ui, -1, '', pos=(10, 50))
        label_en.SetLabel('Hello')


if __name__ == '__main__':
    app = wx.App()
    MyApp(None)
    app.MainLoop()
