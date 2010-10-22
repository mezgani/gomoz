# -*- coding: utf-8 -*- 

import wx, glob
import time
import gmenubar, glistctrl, gtoolbar, gstatusbar
import Gomoz.request as request
import Gomoz.scan 

from wx.py.shell import ShellFrame
from ids import *

import wx.aui, wx.lib.scrolledpanel


class InterGomoz(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Frame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, *args, **kwds)

        ico="Gomoz/image/scf.ico"
        self.icon = wx.Icon(ico, wx.BITMAP_TYPE_ICO) 
        self.SetIcon(self.icon)

        self.c_stack={}
        self.r_stack=[0]

        # The notebook              
        self.notebook = wx.aui.AuiNotebook(self)
        self.notebook.SetBackgroundColour('green')
        
        self.notebook_panel_console = wx.Panel(self.notebook, -1)
        self.notebook_panel_scan = wx.Panel(self.notebook, -1)
        
        # Main staticbox 
        self.sizer_top_staticbox = wx.StaticBox(self, -1, _("Main"))
        self.sizer_top_staticbox.SetForegroundColour('blue')

        #self.menulogic=False
        self.lc_sources=None
        #self.editable = False

        
        self.SetToolBar(self.lc_sources)
        self.__initialize_interframe()
        self.SetGomozMenuBar(self.lc_sources)
        
        
    def _checklist(self):
        self.__initialize_checklist()

    def __initialize_checklist(self):
        self.checklister=glistctrl.CheckListCtrl(self, self.notebook_panel_scan, self.lc_sources)


    def __initialize_interframe(self):
        self.__set_properties()
        self.__initialize_checklist()
        self.__do_layout()        


    def SetGomozMenuBar(self, sources):
        self.menu=gmenubar.GomozMenuBar(self, '' ,sources)
        self.menu.SetCbTarget(self.cb_targets)
        self.menu.SetCbProxy(self.cb_proxy)
        self.menu.SetCbExploit(self.cb_exploit)
        
 
    def SetToolBar(self, sources):
        self.tool=gtoolbar.GomozToolBar(self, '', sources)
        self.tool.__initialize__()
        
  
    """
    def OnAdd(self, event):
        num_items = self.lc_sources.GetItemCount()
        self.lc.InsertStringItem(num_items, self.tc1.GetValue())
        self.lc.SetStringItem(num_items, 1, self.tc2.GetValue())
        self.tc1.Clear()
        self.tc2.Clear()
        """
        
    def __init_statusbar(self):
        """Creates a status bar for main frame"""
        self.statusbar=gstatusbar.GomozStatusBar(self)
        self.SetStatusBar(self.statusbar)
     

    def OnGetRows(self):
        """return index of rows self.lc_sources.GetItemCount()"""
        index = self.lc_sources.GetFirstSelected()
        if index == -1:
            return
        while index != -1:
            item = self.lc_sources.GetItem(index)
            return item.GetText()
            index = self.lc_sources.GetNextSelected(index)

    def OnGetAllRows(self):
        """return number of rows self.lc_sources.GetItemCount()"""
        index = self.lc_sources.GetFirstSelected()
        if index == -1:
            return
        tab=[]
        while index != -1:
            item = self.lc_sources.GetItem(index)
            data=item.GetText()
            tab.append(data)
            index = self.lc_sources.GetNextSelected(index)
       
    def GetServerLogo(self, path):
        if path is None or path == "":
            path="Gomoz/image/smicon02.png"

        logo = wx.ImageList(16,16, True)
        bmp  = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.logo_max = logo.Add(bmp)
        self.lc_sources.AssignImageList(logo, wx.IMAGE_LIST_SMALL)
        
        
    def OnStartScan(self, event):
        choices=["cb_input" , "cb_single" , "cb_glob", "cb_mass"]
        for i in choices:
            req="%s=self.%s.GetValue()" % (i,i)
            exec(req)
        if cb_input==True and cb_single==False and cb_glob == False and cb_mass==False: 
            target=[self.cb_targets.GetValue()]
            exploit=[self.cb_exploit.GetValue()]
            self.CheckScan(target, exploit, "input")
        elif cb_single==True and cb_input==False and cb_glob == False and cb_mass==False: 
            target=[self.cb_targets.GetValue()]
            if self.cb_exploit.GetValue() not in self.cb_exploit.GetItems():
                exploit = [self.cb_exploit.GetValue()]
                exploit +=self.cb_exploit.GetItems()
            else: exploit=self.cb_exploit.GetItems()
            self.CheckScan(target, exploit,"single")
        elif cb_glob==True and cb_input==False and cb_single == False and cb_mass==False: 
            if self.cb_targets.GetValue() not in self.cb_targets.GetItems():
                target = [self.cb_targets.GetValue()]
                target += self.cb_targets.GetItems()
            else: target=self.cb_targets.GetItems()
            exploit=[self.cb_exploit.GetValue()]
            self.CheckScan(target, exploit,"glob")
        elif cb_mass==True and cb_input==False and  cb_single==False and cb_glob ==False: 
            target=[self.cb_targets.GetValue()]
            if self.cb_exploit.GetValue() not in self.cb_exploit.GetItems():
                exploit = [self.cb_exploit.GetValue()]
                exploit +=self.cb_exploit.GetItems()
            else: exploit=self.cb_exploit.GetItems()
            if self.cb_targets.GetValue() not in self.cb_targets.GetItems():
                target = [self.cb_targets.GetValue()]
                target += self.cb_targets.GetItems()
            else: target=self.cb_targets.GetItems()
            self.CheckScan(target, exploit, "mass")
            
        else:
            wx.MessageBox("Please choose one scan option.","Info")
            

    def InputScan(self, req, status):
        defaultx=""
        default =""
        if self.cb_exploit.GetValue() != default or self.cb_targets.GetValue() !=default :
            num_items = self.lc_sources.GetItemCount()
           
            timer=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.lc_sources.InsertStringItem(num_items, str(req))
            self.lc_sources.SetStringItem(num_items, 1, self.cb_targets.GetValue())
            self.lc_sources.SetStringItem(num_items, 2, self.cb_exploit.GetValue())
            self.lc_sources.SetStringItem(num_items, 3, str(timer))
            self.lc_sources.SetStringItem(num_items, 4, status)
        elif self.cb_exploit.GetValue().strip() == '' or self.cb_targets.GetValue().strip() == '' :
            wx.MessageBox("Please Enter correct value.","Info")
            
        else:
            wx.MessageBox("Please Enter correct value.","Info")


    def InputScansOn(self, req, target, exploit, status):
        
            timer=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.lc_sources.InsertStringItem(num_items, str(req))
            self.lc_sources.SetStringItem(num_items, 1, str(target))
            self.lc_sources.SetStringItem(num_items, 2, str(exploit))
            self.lc_sources.SetStringItem(num_items, 3, str(timer))
            self.lc_sources.SetStringItem(num_items, 4, status)

            
    def GetID(self):
        self.counter=0
        self.r_stack.sort()
        if self.r_stack != [0]:
            print int(self.r_stack[-1:][0])
            counter=int(self.r_stack[-1:][0]) + 1

        else:
            counter= 1
        self.r_stack.append(counter)
        return counter


    def CheckScan(self, target, exploit, mode):
        if '' in target:
            target.remove('')
        if '' in exploit:
            exploit.remove('')
        try:
           fs=open("Gomoz/config/gomoz.cfg", 'r')
           while 1:
             txt=fs.readline()
             
             if txt == '':
                break
             if txt[0]!='#': 
                if txt.find('PHPinc') != -1:
                    phpinc=txt.split('=')[1].strip()             
                if txt.find('TXTinc') != -1:
                    txtinc=txt.split('=')[1].strip()
                if txt.find('JPGinc') != -1:
                    jpginc=txt.split('=')[1].strip()
                if txt.find('ASPinc') != -1:
                    aspinc=txt.split('=')[1].strip()
                if txt.find('JSPinc') != -1:
                    jspinc=txt.split('=')[1].strip()                        
                if txt.find('KEYword') != -1:
                    keyword=txt.split('=')[1].strip()
                if txt.find('OPTscan') != -1:
                    scan=txt.split('=')[1].strip()
           fs.close()
        except Exception, e:
            wx.MessageBox(str(e),"Info")
    
        print self.cb_proxy.GetValue()

        slfinc=txtinc.split('.txt')[0]
        r1=request.Request(0, target, "", "/", exploit, phpinc)
        r2=request.Request(0, target, "", "/", exploit, phpinc+'?')
        r3=request.Request(0, target, "", "/", exploit, txtinc)
        r4=request.Request(0, target, "", "/", exploit, txtinc)
        r5=request.Request(0, target, "", "/", exploit, slfinc)
        r6=request.Request(0, target, "", "/", exploit, slfinc+'?')
        r7=request.Request(0, target, "", "/", exploit, jpginc)
        r8=request.Request(0, target, "", "/", exploit, jpginc+'?')
        r9=request.Request(0, target, "", "/", exploit, aspinc)
        r10=request.Request(0, target, "", "/", exploit, aspinc+'?')
        r11=request.Request(0, target, "", "/", exploit, jspinc)
        r12=request.Request(0, target, "", "/", exploit, jspinc+'?')

        """for i in range(1,3):
            req1="r%s.set%s()" % (i,mode)
            req2="r%s.start()" % i
            exec(req1)
            exec(req2)
            """    
        
        start=time.time()

       
        """tempo  = r1.stack + r2.stack + r3.stack + r4.stack 
        tempo += r5.stack + r6.stack + r7.stack + r8.stack"""
        
        exploit = r1.exploit
        target  = r1.target
        path    = r1.directory
        r1.scan()

       
        fd=open('Gomoz/log/gomoz.log','a')          
        try:
            k = 0
            v = 0
            
            #for url in r1.stack:
            #for i in range(len(target)):
             
            for host in target:   
   
                owned=False
                print "[+] "+url
                t=url.replace('http://','')
                if ':' in t:
                    port = host.split(':')[1].split('/')[0]
                    host = host.split(':')[0]
                elif '/' in host:
                    host = host.split('/')[0]
                    port = 80
                else: port = 80
               
                s=Gomoz.scan.ScanOne(host, port)
                result = s.GetResult()
                #if s[port] != "open":
                if result != "open":
                    status = "no response"
                    data = None
                else:    
                    data=r1.wget(url)
                
                snapshot=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
 
                if data is None or data=="":
                    if status != "no response":
                        status='not vulnerable'
                elif data == 1:
                    status='page not found'
                else:
                     if data.find(keyword) == -1:
                         status='not vulnerable'
                     else:
                         status='vulnerable'
                         owned=True
                fd.write("["+snapshot+"] "+url+" ["+status+"] "+"\n")  
                

                if owned==True:
                    status='vulnerable'
                    #self.frame.lc_sources.SetItemTextColour(index, colour)
                    v =+ 1
                a, b=len(target), len(exploit)
                print a,b
                try:
                    if (k*a*b % ((a^k) * (b^k)))==0:
                        #for i in range(len(target)):
                        #    for j in range(len(exploit)):
                                num_items = self.lc_sources.GetItemCount() 
                                req=self.GetID()
                                exploit[j] = path + exploit[j]
                                timer=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                self.lc_sources.InsertStringItem(num_items, str(req))
                                self.lc_sources.SetStringItem(num_items, 1, str(target[i]))
                                self.lc_sources.SetStringItem(num_items, 2, str(exploit[j]))
                                self.lc_sources.SetStringItem(num_items, 3, str(timer))
                                if status=="not vulnerable":
                                    index = self.lc_sources.GetFocusedItem()
                                    if index == -1:
                                       index = 0
                                    color=(255,0,0,255)
                                    self.lc_sources.SetItemTextColour(index+num_items, color)
                                self.lc_sources.SetStringItem(num_items, 4, status)
                                self.statusbar.SetStatusText(str(exploit[j]), 0)
                                end=time.time()
                                s=("%.3f" % float(end-start))
                                self.statusbar.WriteStatus(str(s)+" sec", 3)
                                self.statusbar.WriteStatus(str("Scanning ..."), 1)
                                k += 1
                                exploit[j]=exploit[j][len(path):].replace(path, '')
                            
                except Exception, e:
                    print(str(e))
                    raise(e)
            t=len(exploit)*len(target)
            
            self.statusbar.WriteStatus(str("Scan finished"), 0)
            msg=str(t)+" URL scanned"
            self.statusbar.WriteStatus(str(msg), 1)

            
            self.statusbar.WriteStatus(str(v)+" URL vulnerable(s)",2)
           
        except AttributeError, e :
            print (str(e))
        except Exception, ex :
            print (str(ex))


    def __set_properties(self):
        # begin wxGlade: Frame.__set_properties
        self.__init_statusbar()
        self.SetTitle(_("GOMOZ"))
        self.SetSize((800, 600))
        self.label_1 = wx.StaticText(self, -1, _("Timer:"))
        #self.label_1.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.label_1.SetForegroundColour('black')

        self.label_timer=wx.StaticText(self, -1, '00:00:00:00')
        self.label_timer.SetForegroundColour('red')

        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()

        
        self.label_2 = wx.StaticText(self, -1, ("Hosts:"))
        self.label_2.SetForegroundColour('black')       
        self.cb_targets = wx.ComboBox(self, -1, "", choices=[""], style=wx.CB_DROPDOWN|wx.CB_SORT)
        
        self.cb_targets.SetBackgroundColour(wx.BLACK)
        self.cb_targets.SetForegroundColour(wx.GREEN)
        self.cb_targets.SetValue("")
        
        self.label_4 = wx.StaticText(self, -1, ("Scan:"))
        #self.label_4.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.label_4.SetForegroundColour('black')
        
        self.cb_input = wx.CheckBox(self, -1, ("Input"))
        self.cb_single = wx.CheckBox(self, -1, ("Single"))
        self.cb_mass = wx.CheckBox(self, -1, ("Mass"))
        self.cb_glob = wx.CheckBox(self, -1, ("Global"))
        
        """self.cb_input.SetForegroundColour('red')
        self.cb_input.SetBackgroundColour('black')
        self.cb_single.SetForegroundColour('red')
        self.cb_single.SetBackgroundColour('black')
        self.cb_glob.SetForegroundColour('red')
        self.cb_glob.SetBackgroundColour('black')
        self.cb_mass.SetForegroundColour('red')
        self.cb_mass.SetBackgroundColour('black')
        """
        self.cb_input.SetValue(0)
        self.cb_single.SetValue(1)
        self.cb_glob.SetValue(0)
        self.cb_mass.SetValue(0)

        self.label_5 = wx.StaticText(self, -1, ("Path    :"))
        #self.label_5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.label_5.SetForegroundColour('black')

        self.tc_url = wx.TextCtrl(self, -1, ("/"))
        self.tc_url.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.tc_url.SetBackgroundColour(wx.WHITE)
        self.tc_url.SetForegroundColour(wx.BLACK)

    
        self.label_6 = wx.StaticText(self, -1, ("Proxy   :"))
        #self.label_6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.label_6.SetForegroundColour('black')
        
        self.cb_proxy = wx.ComboBox(self, -1, choices=[""], style=wx.CB_DROPDOWN|wx.CB_SORT)
        #self.cb_proxy.SetSelection(1)
        self.cb_proxy.SetBackgroundColour(wx.BLACK)
        self.cb_proxy.SetForegroundColour(wx.GREEN)
        #self.cb_proxy.SetValue("proxy:port")
    
        self.label_7 = wx.StaticText(self, -1, ("Exploit :"))
        #self.label_7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.label_7.SetForegroundColour('black')
            
        self.cb_exploit = wx.ComboBox(self, -1, choices=[""], style=wx.CB_DROPDOWN|wx.CB_SORT)
        #self.cb_exploit.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.cb_exploit.SetBackgroundColour(wx.BLACK)
        self.cb_exploit.SetForegroundColour(wx.GREEN)
        self.cb_exploit.SetValue("")  
    
        # in case we are recreating the list tickle the frame a bit so
        # it will redo the layout
        self.SendSizeEvent()
        

    def Stop(self):
        self.timer.stop()
        del self.timer
        
    def Notify(self):
        t = time.localtime(time.time())
        st = time.strftime("%I:%M:%S %p", t)
        # --- could also use self.sb.WriteStatus
        self.label_timer.SetLabel(st)
        #self.statusbar.WriteStatus(st)

    

    def __do_layout(self):
        # begin wxGlade: Frame.__do_layout
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_top = wx.StaticBoxSizer(self.sizer_top_staticbox, wx.HORIZONTAL)
        grid_sizer_2 = wx.FlexGridSizer(3, 2, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(4, 2, 0, 0)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(self.label_1, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        grid_sizer_1.Add(self.label_timer, 1, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        grid_sizer_1.Add(self.label_2, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        grid_sizer_1.Add(self.cb_targets, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        grid_sizer_1.Add(self.label_4, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)

        sizer_2.Add(self.cb_input, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)
        sizer_2.Add(self.cb_single, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)
        sizer_2.Add(self.cb_glob, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)
        sizer_2.Add(self.cb_mass, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)

        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_1.AddGrowableCol(1)
        sizer_top.Add(grid_sizer_1, 1, wx.ALL|wx.EXPAND, 3)
        grid_sizer_2.Add(self.label_5, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        grid_sizer_2.Add(self.tc_url, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        grid_sizer_2.Add(self.label_6, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        grid_sizer_2.Add(self.cb_proxy, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        grid_sizer_2.Add(self.label_7, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 3)
        grid_sizer_2.Add(self.cb_exploit, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        grid_sizer_2.AddGrowableCol(1)
        sizer_top.Add(grid_sizer_2, 1, wx.ALL|wx.EXPAND, 3)
        sizer_base.Add(sizer_top, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 3)
        sizer_3.Add(self.lc_sources, 1, wx.EXPAND, 0)

        
        self.notebook_panel_scan.SetAutoLayout(True)
        self.notebook_panel_scan.SetSizer(sizer_3)
        sizer_3.Fit(self.notebook_panel_scan)
        sizer_3.SetSizeHints(self.notebook_panel_scan)
        self.notebook.AddPage(self.notebook_panel_scan, _("Scans"))
        sizer_base.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 3)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_base)
        self.Layout()
        self.Centre()
        # end wxGlade

    def SetNameConsole(self, tab, name):
        tab.SetName(name)        


    def OnConsole(self, event):
        console=self.OnGetRows()
        if console is None or console =="":
            console="Unnamed"
        self.notebook_console = wx.Panel(self.notebook, -1)
        self.notebook_console.SetAutoLayout(True)
        self.notebook_console.SetBackgroundColour('wx.BLACK')
        self.notebook.AddPage(self.notebook_console, (console))
        self.notebook_console.SetForegroundColour(wx.WHITE)
        
        #the name of tab, has to be checked
        self.label=wx.StaticText(self.notebook_console, -1, ("["+console+"]$ _"))
        self.label.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.Refresh()       


    def OnChoice(self, event=None):
        data = []
	self.target  = self.cb_targets.GetStringSelection()
	self.url  = self.tc_url.GetStringSelection()
	self.proxy = self.cb_proxy.GetStringSelection()
	self.exploit   = self.cb_exploit.GetStringSelection()
	if  self.target != "" and self.exploit != "":
		data.append(0)
		data.append(self.target)
		data.append(self.exploit)
		data.append('date')
		data.append('started')
		return data
	else:
		return -1
        
    
    

