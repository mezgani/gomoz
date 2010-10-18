import wx
import cmd

class GomozConsole:
    def __init__(self, panel, id, title):
        self.panel = panel
        vbox=wx.BoxSizer(wx.HORIZONTAL)
        panel.SetBackgroundColour('black')
        self.output = wx.TextCtrl(panel, -1, "[target]$ ", size=(780,320), style = wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        self.output.SetFont(wx.Font(8, wx.SWISS,wx.NORMAL, wx.BOLD))
        self.output.SetForegroundColour('white')
        self.output.SetBackgroundColour('black')
        self.output.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown,self.output)
        
        vbox.Add(self.output, 1, wx.ALL|wx.EXPAND, 1)
        

        
        self.x=0
        self.y=0
        
        self.text=''
        self.lock=True


    def SetParams(self, url, exploit, proxy):
        self.url=url
        self.exploit=exploit
        self.proxy=proxy

        
    def OnKeyDown(self, event):

        keycode = event.GetKeyCode()          
        if keycode == wx.WXK_RETURN:
           self.x=self.output.GetLastPosition() 
           msg="[target]$ "
           self.output.AppendText(msg) 
           self.output.SetInsertionPoint(self.x)
      
           self.x=self.output.GetLastPosition()
           self.y=self.output.GetLineLength(self.x)
           (start, end) = self.output.GetSelection()
           (scol, sline) = self.output.PositionToXY(start)
           self.text=self.output.GetLineText(sline)

           print self.x, self.y,self.text
           #spider=cmd.exploiter(self.exploit, self.proxy, self.url)
           #spider.SetCmd(str(self.text))
           #data=spider.run()
           #self.output.AppendText(data)
           
           if self.text.strip()=='clear':
              self.output.Clear() 

        
        if keycode == wx.WXK_ESCAPE:
            ret  = wx.MessageBox('Are you sure to quit?', 'Question', wx.YES_NO | wx.NO_DEFAULT, self.panel)
            if ret == wx.YES:
                import interwin
                interwin.InterGomoz.r_stack[1].Close()
                self.panel.Close()
                
        event.Skip()

