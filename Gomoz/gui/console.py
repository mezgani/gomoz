import wx
import cmd
import subprocess

class GomozConsole(wx.Panel):
    #def __init__(self, panel, *args, **kwds):
    def __init__(self, parent, id, title):
        wx.Panel.__init__(self, parent=parent)
        self.panel = parent
        self.prompt = "user@stackOvervlow:~ "
        self.textctrl = wx.TextCtrl(self.panel, -1, '', size=(980,700), style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        self.default_txt = self.textctrl.GetDefaultStyle()
        self.textctrl.AppendText(self.prompt)
        self.textctrl.SetForegroundColour('white')
        self.textctrl.SetBackgroundColour('black')
        """self.textctrl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown,self.textctrl)"""
        

        self.__set_properties()
        self.__do_layout()
        self.__bind_events()


    def __bind_events(self):
        self.Bind(wx.EVT_TEXT_ENTER, self.__enter)


    def __enter(self, e):

        self.value = (self.textctrl.GetValue())
        print (self.value)
        self.eval_last_line()
        e.Skip()


    def __set_properties(self):
        #self.SetTitle("Poor Man's Terminal")
        self.SetSize((800, 600))
        self.textctrl.SetFocus()

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.textctrl, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

    def eval_last_line(self):
        nl = self.textctrl.GetNumberOfLines()
        ln = self.textctrl.GetLineText(nl-1)
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


            
    def OnKeyDown(self, event):
        keycode = event.GetKeyCode() 
        if keycode == wx.WXK_ESCAPE:
            ret  = wx.MessageBox('Are you sure to quit?', 'Question', wx.YES_NO | wx.NO_DEFAULT, self.panel)
            if ret == wx.YES:
                import interwin
                interwin.InterGomoz.r_stack[1].Close()
                self.panel.Close()
                
        event.Skip()

