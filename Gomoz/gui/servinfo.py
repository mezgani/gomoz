import wx


class InfoFrame(wx.Frame):
    def __init__(self,*args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        ico="Gomoz/image/scf.ico"
        self.icon = wx.Icon(ico, wx.BITMAP_TYPE_ICO) 
        self.SetIcon(self.icon)
        self.panel = wx.Panel(self, -1, size=(400, 320))
        self.text=''
        #self.panel.SetBackgroundColour('black')

        self.output = wx.TextCtrl(self, -1, self.text, size=(360,250),pos=(10,10),style=wx.TE_MULTILINE)
        self.output.SetBackgroundColour('black')
        self.output.SetForegroundColour('green')
        self.output.SetEditable(True)


        self.button = wx.Button(self.panel, id=-1, pos=(160, 260))
        self.button.SetLabel('copy')
        #self.button.SetBackgroundColour('black')
        #self.button.SetForegroundColour('green')
        self.button.Bind(wx.EVT_BUTTON, self.CopyText)

    def SetText(self, text):
        self.output.WriteText(text)


    def CopyText(self,event):
        self.output.SelectAll()
        self.output.Copy()


