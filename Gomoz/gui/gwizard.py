import wx
import wx.wizard

class GomozIntroCgf(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.title=title
       
    


class FirstPage(GomozIntroCgf):
    def __init__(self, wizard, title):
        GomozIntroCgf.__init__(self, wizard, "Gomoz Config")
        self.title=title
        self.data={}
        self.error=''
        self.phpinc=''
        self.txtinc=''
        self.aspinc=''
        self.jspinc=''
        self.jpginc=''
        self.keyword=''
        self.scan=''
        self.SetData('Gomoz/config/gomoz.cfg')
        
        self.label_2=wx.StaticText(self, -1, "include.PHP", pos=(10, 130))
        self.input_2=wx.TextCtrl(self, -1, self.phpinc, size=(180,20),pos=(80,130))

        self.label_3=wx.StaticText(self, -1, "include.TXT", pos=(10, 160))
        self.input_3=wx.TextCtrl(self, -1, self.txtinc, size=(180,20),pos=(80,160))
        
        self.label_4=wx.StaticText(self, -1, "include.JPG", pos=(10, 190))
        self.input_4=wx.TextCtrl(self, -1, self.jpginc, size=(180,20),pos=(80,190))

        self.label_5=wx.StaticText(self, -1, "include.ASP", pos=(10, 220))
        self.input_5=wx.TextCtrl(self, -1, self.aspinc, size=(180,20),pos=(80,220))
        
        self.label_6=wx.StaticText(self, -1, "include.JSP", pos=(10, 250))
        self.input_6=wx.TextCtrl(self, -1, self.jspinc, size=(180,20),pos=(80,250))

        self.label_7=wx.StaticText(self, -1, "KeyWord", pos=(10, 280))
        self.input_7=wx.TextCtrl(self, -1, self.keyword, size=(180,20),pos=(80,280))



        for i in range(2,8):
            text="self.label_%s.SetForegroundColour(\"black\")" % i
            exec(text)
            #bg="self.input_%s.SetBackgroundColour(wx.BLACK)" % i
            #fg="self.input_%s.SetForegroundColour(wx.GREEN)" % i
            #exec(bg)
            #exec(fg)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.c99 = wx.CheckBox(self, -1, ("C99 Backdoor"))
        self.r57 = wx.CheckBox(self, -1, ("R57 Backdoor"))
        self.others = wx.CheckBox(self, -1, ("Other"))

        if self.scan=='c99': self.c99.SetValue(True)
        elif self.scan=='r57': self.r57.SetValue(True)
        elif self.scan=='others': self.others.SetValue(True)
        else:
            self.scan=''
        
        self.c99.SetForegroundColour('red')
        #self.c99.SetBackgroundColour('black')
        self.r57.SetForegroundColour('red')
        #self.r57.SetBackgroundColour('black')
        self.others.SetForegroundColour('red')
        #self.others.SetBackgroundColour('black')
    

        self.hbox.Add(self.c99)
        self.hbox.Add(self.r57, 0, wx.LEFT, 10)
        self.hbox.Add(self.others)
        
        self.vbox.Add(self.hbox,0 , wx.ALL,5)
        
        self.vbox.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        
        fgs = wx.FlexGridSizer(3, 2, 5, 5)
        fgs.Add(self.label_2, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.input_2, 0, wx.EXPAND)
        fgs.Add(self.label_3, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.input_3, 0, wx.EXPAND)
        fgs.Add(self.label_4, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.input_4, 0, wx.EXPAND)
        fgs.Add(self.label_5, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.input_5, 0, wx.EXPAND)
        fgs.Add(self.label_6, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.input_6, 0, wx.EXPAND)
        fgs.Add(self.label_7, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.input_7, 0, wx.EXPAND)


        fgs.AddGrowableCol(1)
        self.vbox.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
        
        self.Layout()

    def SetData(self, path):
        try:
           fs=open(path, 'r')
           while 1:
             txt=fs.readline()
             
             if txt == '':
                break
             if txt[0]!='#': 
                if txt.find('PHPinc') != -1:
                    self.phpinc=txt.split('=')[1].replace('\n','')
                   
                if txt.find('TXTinc') != -1:
                    self.txtinc=txt.split('=')[1].replace('\n','')

                if txt.find('ASPinc') != -1:
                    self.aspinc=txt.split('=')[1].replace('\n','')
                   
                if txt.find('JSPinc') != -1:
                    self.jspinc=txt.split('=')[1].replace('\n','')

                if txt.find('JPGinc') != -1:
                    self.jpginc=txt.split('=')[1].replace('\n','')
                    
                if txt.find('KEYword') != -1:
                    self.keyword=txt.split('=')[1].replace('\n','')
                    
                if txt.find('OPTscan') != -1:
                    self.scan=txt.split('=')[1].replace('\n','')
                    
           fs.close()
        except:
            pass
    


    def Layout(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.staticbox = wx.StaticBox(self, -1, (self.title))
        self.staticbox.SetForegroundColour('blue')
        self.sizz=wx.StaticBoxSizer(self.staticbox, wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.text="""To setup scan option, we must make up all var in the forms follow."""
        titleText = wx.StaticText(self, -1, self.text)
        titleText.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.BOLD))
        #titleText.SetForegroundColour("green")
        self.sizz.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        #self.sizz.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.sizz, 0, wx.EXPAND | wx.ALL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        top_staticbox = wx.StaticBox(self, -1, ("scan options"))
        top_staticbox.SetForegroundColour('blue')
        sizer_top = wx.StaticBoxSizer(top_staticbox, wx.HORIZONTAL)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.vbox, 0, wx.LEFT, 10)
        #self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        sizer_top.Add(sizer, 1, wx.ALL|wx.EXPAND, 1)
        self.sizer.Add(sizer_top, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 4)


    def GetCheckBox(self):
        self.data['OPTscan']=None
        if self.c99.GetValue()==True and self.r57.GetValue()==False and self.others.GetValue()==False:
            self.data['OPTscan']="c99"
        elif self.r57.GetValue()== True and self.c99.GetValue()==False and self.others.GetValue()==False:
            self.data['OPTscan']="r57"
        elif self.others.GetValue()==True and self.r57.GetValue()==False and self.c99.GetValue()==False:
            self.data['OPTscan']="others"
        else:
            self.error='Please choose one scan option.'
            
        

    def GetData(self):
        self.GetCheckBox()

        if self.input_2.GetValue().strip() != '':
           self.data['PHPinc']=self.input_2.GetValue()
        else:
           self.error="Please complete the PHPinc input ."
           
        if self.input_3.GetValue().strip() != '':
           self.data['TXTinc']=self.input_3.GetValue()
        else:
           self.error="Please complete the TXTinc input ."

        if self.input_4.GetValue().strip() != '':
           self.data['JPGinc']=self.input_4.GetValue()
        else:
           self.error="Please complete the JPGinc input ."
           
        if self.input_5.GetValue().strip() != '':
           self.data['ASPinc']=self.input_5.GetValue()
        else:
           self.error="Please complete the ASPinc input ."
           
        if self.input_6.GetValue().strip() != '':
           self.data['JSPinc']=self.input_6.GetValue()
        else:
           self.error="Please complete the JSPinc input ."

        if self.input_7.GetValue().strip() != '':
            self.data['KEYword']=self.input_7.GetValue()
        else:
           self.error="Please complete the keyword input ."
           
            
        if self.error != '':
               wx.MessageBox(self.error,"info")
               
        else:
             return self.data


      

class LastPage(GomozIntroCgf):
    def __init__(self, wizard, title):
        GomozIntroCgf.__init__(self, wizard, "Gomoz Config")
        self.title=title


        text1="Native LABS will not be held responsible for any loss, damages, accident,"
        text2="hardware failures, network failures or sabotage."
        self.label_1=wx.StaticText(self, -1, text1, pos=(10,130))
        self.label_2=wx.StaticText(self, -1, text2, pos=(10,160))
                
        image="Gomoz/image/gomoz1.png"
        imag = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.button = wx.StaticBitmap(self, id=-1, bitmap=imag, pos=(420, 20), size = (imag.GetWidth(), imag.GetHeight()-5))
        self.radioList=["Accept", "Decline"]
        self.r1=wx.RadioBox(self, -1, "Important",wx.Point(10, 210), wx.DefaultSize,self.radioList, 3, wx.RA_SPECIFY_COLS)
        self.r1.SetSelection(1)
        self.Layout()




    def SetLabel(self, label, pos):
        text=wx.StaticText(self, -1, label, pos=pos)
        text.SetForegroundColour("blue")


    def Layout(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.staticbox = wx.StaticBox(self, -1, (self.title))
        self.staticbox.SetForegroundColour('blue')
        self.sizz=wx.StaticBoxSizer(self.staticbox, wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        self.sizer.Add(self.sizz, 0, wx.EXPAND | wx.ALL, 5)
        self.sizz.Add(self.r1, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        

        sizer = wx.BoxSizer(wx.VERTICAL)
        top_staticbox = wx.StaticBox(self, -1, ("Legal information"))
        top_staticbox.SetForegroundColour('blue')
        sizer_top = wx.StaticBoxSizer(top_staticbox, wx.HORIZONTAL)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.button)
        sizer1.Add(self.label_1)
        sizer1.Add(self.label_2)
       
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        sizer_top.Add(sizer, 1, wx.ALL|wx.EXPAND, 1)
        self.sizer.Add(sizer_top, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 4)    



