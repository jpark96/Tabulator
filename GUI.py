import wx

class Example(wx.Frame):
  
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, 
            size=(260, 180))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        panel = wx.Panel(self)

        panel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)

        midPan = wx.Panel(panel)
        midPan.SetBackgroundColour('#ededed')

        vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 5
        	)
        panel.SetSizer(vbox)

        textbox = wx.TextCtrl(midPan)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(textbox, 1, wx.EXPAND | wx.ALL, 10)
        midPan.SetSizer(vbox2)
        

if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title='Border')
    app.MainLoop()