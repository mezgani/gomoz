import wx
import subprocess
import re
import Gomoz.scan.cmd as cmd

class GomozConsole(wx.Panel):
    #def __init__(self, panel, *args, **kwds):
    def __init__(self, parent, id, title, prompt, mode):
        wx.Panel.__init__(self, parent=parent)
        self.panel = parent
        if prompt != "" or prompt is not None:
            self.prompt = prompt
        else:
            self.prompt = "user@gomoz:~ "
        self.textctrl = wx.TextCtrl(self.panel, -1, '', style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        self.mode = mode
        self.default_txt = self.textctrl.GetDefaultStyle()
        self.textctrl.AppendText(self.prompt)
        #self.textctrl.SetForegroundColour('white')
        #self.textctrl.SetBackgroundColour('black')

        self.__set_properties()
        self.__do_layout()
        self.__bind_events(self.mode)
       
    def __bind_events(self, mode):
        if mode=='local':
            self.textctrl.Bind(wx.EVT_TEXT_ENTER, self.__enter)
        else:
            self.textctrl.Bind(wx.EVT_TEXT_ENTER, self.__enter_cmd)

    def __enter_cmd(self, e):
        self.value = (self.textctrl.GetValue())
        self.eval_last_line("")
        e.Skip()

    def __enter(self, e):
        self.value = (self.textctrl.GetValue())
        self.eval_last_line('local')
        e.Skip()


    def __set_properties(self):
        self.textctrl.SetFocus()

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.textctrl, 1, wx.EXPAND |wx.ALL, 0)
        self.panel.SetSizer(sizer_1)
        self.Layout()

    def eval_last_line(self, mode):
        nl = self.textctrl.GetNumberOfLines()
        ln = self.textctrl.GetLineText(nl-1)
        ln = ln[len(self.prompt):]
        args = ln.split(" ")
        if mode=='local':
            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            retvalue = proc.communicate()[0]
        else:
            url="http://localhost/temp/py100.php?cmd="
            stat = cmd.exploiter("","","", url, ln)
            retvalue = stat.GetData()
            retvalue += '\n'
            
        c = wx.Colour(0, 0, 0)
        tc = wx.TextAttr(c)
        self.textctrl.SetDefaultStyle(tc)
        self.textctrl.AppendText('\n')
        self.textctrl.AppendText(retvalue)
        self.textctrl.SetDefaultStyle(self.default_txt)
        self.textctrl.AppendText(self.prompt)
        pos = self.textctrl.GetLastPosition()
        y = self.textctrl.GetNumberOfLines()
        (x, y) = self.textctrl.PositionToXY(self.textctrl.GetLastPosition())
        print x,y
        pos = self.textctrl.XYToPosition(len(self.prompt), nl)
        print pos
        self.textctrl.SetInsertionPoint(GetLastPosition())
        


 
