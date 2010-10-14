import wx

class GomozStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent)
        self.SetFieldsCount(4)
        self.SetStatusText('Welcome to Gomoz', 0)
                
        self.SetStatusWidths([-5, -2, -1,-1])
       

        self.icon = wx.StaticBitmap(self, -1, wx.Bitmap('Gomoz/image/apache.png'))
        self.SetStatusText('0 url(s) scanned', 1)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.PlaceIcon()


    def PlaceIcon(self):
        rect = self.GetFieldRect(2)
        self.icon.SetPosition((rect.x+102, rect.y+3.5))

      
    def OnSize(self, event):
        self.PlaceIcon()
