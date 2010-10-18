import wx
import subprocess

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.prompt = "user@stackOvervlow:~ "
        self.textctrl = wx.TextCtrl(self, -1, '', style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        self.default_txt = self.textctrl.GetDefaultStyle()
        self.textctrl.AppendText(self.prompt)
        

        self.__set_properties()
        self.__do_layout()
        self.__bind_events()


    def __bind_events(self):
        self.Bind(wx.EVT_TEXT_ENTER, self.__enter)


    def __enter(self, e):

        self.value = (self.textctrl.GetValue())
        self.eval_last_line()
        e.Skip()


    def __set_properties(self):
        self.SetTitle("Poor Man's Terminal")
        self.SetSize((800, 600))
        self.textctrl.SetFocus()

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.textctrl, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

    def eval_last_line(self):
        nl = self.textctrl.GetNumberOfLines()
        ln =  self.textctrl.GetLineText(nl-1)
        ln = ln[len(self.prompt):]
        args = ln.split(" ")

        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        retvalue = proc.communicate()[0]

        c = wx.Colour(239, 177, 177)
        tc = wx.TextAttr(c)
        self.textctrl.SetDefaultStyle(tc)
        self.textctrl.AppendText('\n')
        self.textctrl.AppendText(retvalue)
        self.textctrl.SetDefaultStyle(self.default_txt)
        self.textctrl.AppendText(self.prompt)
        self.textctrl.SetInsertionPoint(GetLastPosition() - 1)

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()

