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
##        self.w_idx= wx.StaticBitmap(self, -1,wx.ArtProvider_GetBitmap(wx.ART_WARNING,wx.ART_TOOLBAR,(16,16)))
##        a={"w_idx":"WARNING","e_idx":"ERROR","i_idx":"QUESTION"}
##        for k,v in a.items():
##          s="self.%s= wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16))" % (k,v)
##          exec(s)


    def PlaceIcon(self):
        rect = self.GetFieldRect(2)
        #self.w_idx.SetPosition((rect.x+140, rect.y+0))
        self.icon.SetPosition((rect.x+140, rect.y+0))

      
    def OnSize(self, event):
        self.PlaceIcon()
