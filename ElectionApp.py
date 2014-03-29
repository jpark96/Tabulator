#!/usr/bin/env python
### ElectionApp.py

import wx
from ElectionWindow import *

app = wx.App()
ElectionFrame(None, title='ASUC Tabulator v4.0')
app.MainLoop()