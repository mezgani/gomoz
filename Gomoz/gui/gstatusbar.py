import wx

class GomozStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent)
        self.SetFieldsCount(4)
        #self.SetStatusText('Welcome to Gomoz', 0)
        self.SetStatusWidths([-5, -2, -2,-1])
        #self.icon = wx.StaticBitmap(self, -1, wx.Bitmap('Gomoz/image/apache.png'))
        self.SetStatusText('0 URL Scanned', 1)
        #self.SetBackgroundColour("white")
        self.SetForegroundColour(wx.RED)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.PlaceIcon()
        

    
    def PlaceIcon(self):
        rect = self.GetFieldRect(0)
        self.icon.SetPosition((rect.x+1, rect.y+3.5))
        
      
    def OnSize(self, event):
        pass
        """self.PlaceIcon()"""

    def WriteStatus(self, msg, column):
        if msg is None or column is None:
            pass
        else:
            self.SetStatusText(msg, column)
