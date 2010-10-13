from ids import *
import wx, images
import time
import portscan
import gwizard, ghelp
import glistctrl
import threading
 
class GomozToolBar:
    def __init__(self, frame, panel, sources):

        self.frame = frame
        self.panel = panel
        self.lc_sources = sources

    def __initialize__(self):
        # Tool Bar
        self.frame.toolbar = self.frame.CreateToolBar()
        self.frame.toolbar.AddSeparator()
        #toolbar.AddSimpleTool(wx.NewId(), images.getNewBitmap(),"New", "Long help for 'New'")
        self.frame.toolbar.SetToolBitmapSize(wx.Size(48, 48))
        
      	digicon="Gomoz/image/info.png"
        imag2 = wx.Image(digicon, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #self.button = wx.BitmapButton(self.mainPanel, id=-1, bitmap=imag2, pos=(120, 20), size = (imag2.GetWidth(), imag2.GetHeight()))
        self.frame.toolbar.AddSimpleTool(ID_SCAN_NEW,imag2,"Config gomoz",'Config gomoz')

        
        image="Gomoz/image/new.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.frame.toolbar.AddSimpleTool(ID_SCAN_ADD,imag2,"Add","Add request")
        
        #self.frame.toolbar.AddSimpleTool(ID_SCAN_NEW,images.getNewBitmap(),"New","New file")
        self.frame.toolbar.AddSeparator()
        image="Gomoz/image/tune.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.frame.toolbar.AddSimpleTool(ID_SCAN,imag2,"Start",'Start scan')
	#self.frame.toolbar.AddSimpleTool(ID_SCAN,images.getFindBitmap(),"Start",'Start scan')
	
        image="Gomoz/image/scan.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	self.frame.toolbar.AddSimpleTool(ID_GET_INFO,imag2,"Ports scan",'Ports scan')
	#self.frame.toolbar.AddSimpleTool(ID_GET_INFO,images.getFindDataBitmap(),"Get Info From NCBI",'Get Info')
	self.frame.toolbar.AddSeparator()
	
        image="Gomoz/image/delete.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.frame.toolbar.AddSimpleTool(ID_DELETE,imag2,"Delete request",'Delete request')
	#self.frame.toolbar.AddSimpleTool(ID_DELETE,images.getClearBitmap(),"Delete request",'Delete request')

        image="Gomoz/image/remove.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.frame.toolbar.AddSimpleTool(ID_DELETE_ALL,imag2,"Delete All",'Delete All')
	#self.frame.toolbar.AddSimpleTool(ID_DELETE_ALL,images.getDeleteAllBitmap(),"Delete All",'Delete All')


	self.frame.toolbar.AddSeparator()

    
        image="Gomoz/image/Eterm.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.frame.toolbar.AddSimpleTool(ID_CLOSE,imag2, "Close console",'Close console')
        #self.frame.toolbar.AddSimpleTool(ID_CLOSE,images.getCloseOneBitmap(),"Close console",'Close console')

        image="Gomoz/image/eclipse.png"
        imag2 = wx.Image(image, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	self.frame.toolbar.AddSimpleTool(ID_CLOSE_ALL,imag2,"Close All consoles",'Close All consoles')

        #self.frame.toolbar.AddSimpleTool(ID_CLOSE_ALL,images.getCloseAllBitmap(),"Close All consoles",'Close All consoles')
        #self.frame.toolbar.AddSimpleTool(807, wx.Bitmap('icons/stock_exit.png'), 'Exit', '')

      	self.frame.toolbar.AddSeparator()



        
        digicon="Gomoz/image/Helps.png"
        imag2 = wx.Image(digicon, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.frame.toolbar.AddSimpleTool(ID_HELP,imag2,"Help",'Help')

    
       

        self.frame.Bind(wx.EVT_TOOL, self.OnNewScan, id=ID_SCAN_NEW)
        self.frame.Bind(wx.EVT_TOOL, self.OnAdd, id=ID_SCAN_ADD)
        self.frame.Bind(wx.EVT_TOOL, self.frame.OnStartScan, id=ID_SCAN)
        self.frame.Bind(wx.EVT_TOOL, self.OnRemove, id=ID_DELETE)
        self.frame.Bind(wx.EVT_TOOL, self.OnRemoveAll, id=ID_DELETE_ALL)
        self.frame.Bind(wx.EVT_TOOL, self.OnPortScan, id=ID_GET_INFO)
        self.frame.Bind(wx.EVT_TOOL, self.OnCloseConsole, id=ID_CLOSE)
        self.frame.Bind(wx.EVT_TOOL, self.OnCloseAll, id=ID_CLOSE_ALL)
        self.frame.Bind(wx.EVT_TOOL, self.OnHelp, id=ID_HELP)
        
        self.frame.toolbar.Realize()
        self.frame.toolbar.SetBackgroundColour('black')
        #self.frame.toolbar.SetForegroundColour('white')


    def OnHelp(self, event):
        app=wx.App()
        frm = ghelp.HtmlHelp(self.frame)
        frm.OnShowHelpContents()
        app.MainLoop()
        

    def OnCloseConsole(self, event):
        self.CloseConsole(10)

        

    def CloseConsole(self, request):
        self.frame.c_stack[request].Close()
        del self.frame.c_stack[request]
    def OnCloseAll(self, event):
        for i in self.frame.c_stack:
            self.frame.c_stack[i].Close()
        self.frame.c_stack={}

            
    def OnNewScan(self,event=None):
        request="Do you really want to delete all?"
        title="Delete all"
        if wx.MessageBox(request,title,wx.ICON_QUESTION|wx.YES_NO,self.frame) == wx.YES:
          item=self.frame.lc_sources.GetItemCount()
          self.frame.lc_sources.DeleteAllItems()
          self.frame.cb_exploit.Clear()
          self.frame.cb_targets.Clear()
          self.frame.cb_proxy.Clear()
          self.frame.cb_single.SetValue(0)
          self.frame.cb_mass.SetValue(0)
          self.frame.cb_glob.SetValue(0)
          self.frame.tc_url.Clear()
          self.frame.r_stack=[0]
          #clear consoles
          #set timer 00
        else:
          #self.OnSave
          pass
        
        #app = wx.PySimpleApp()
       
            
        wizard = wx.wizard.Wizard(None, -1, "Gomoz setup scan")
        page1 = gwizard.FirstPage(wizard,"Gomoz setup scan")
        page1.SetBackgroundColour('black')
        page1.SetForegroundColour('green')
   
        page2 = gwizard.LastPage(wizard,"Gomoz and laws")
        page2.SetBackgroundColour('white')
        page2.SetForegroundColour('blue')
    
        wx.wizard.WizardPageSimple_Chain(page1, page2)
       
        wizard.FitToPage(page1)

        if wizard.RunWizard(page1):
            data=page1.GetData()
            if page2.r1.GetStringSelection()=='Accept':
               if data is not None: 
                   fd=open("Gomoz/config/gomoz.cfg",'w')
                   fd.write('############Gomoz scan config file#############\n')
                   fd.write('# Gomoz scanner v 1.0.1\n')
                   fd.write('# Comment different directive for a new setting\n')
                   fd.write('###############################################\n')
                   for k,v in data.items():
                       fd.write(k+'='+v+'\n')
                   fd.close()
            else:
                exit(-1)
        else:
            return
        wizard.Destroy()
          
    def OnShell(self, event):
        frame = ShellFrame(parent=self)
        frame.Show()

    def OnAdd(self, event):
       
        #glistctrl.CheckListCtrl.SetImageServer(self.frame.checklister,'apache')
        num_items = self.frame.lc_sources.GetItemCount()
        counter=self.frame.GetID()
        timer=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.frame.cb_targets.GetValue()!="Enter target" and self.frame.cb_exploit.GetValue()!="Load exploits from file":    
           self.frame.lc_sources.InsertStringItem(num_items, str(counter))
           self.frame.lc_sources.SetStringItem(num_items, 1, self.frame.cb_targets.GetValue())
           self.frame.lc_sources.SetStringItem(num_items, 2, self.frame.cb_exploit.GetValue())
           self.frame.lc_sources.SetStringItem(num_items, 3, str(timer))
           self.frame.lc_sources.SetStringItem(num_items, 4, "unknown")
           #self.tc1.Clear()
           #self.tc2.Clear()

    def OnPortScan(self, event):
       target=None 
       try:
           index=self.frame.lc_sources.GetFirstSelected()
                 
           if index==-1:
              pass
           if index != -1:
              index=self.frame.lc_sources.GetFocusedItem()
              target=self.frame.lc_sources.GetItem(index, 1).GetText()
              if target.split(':'):
                  target=target.split(':')[0]
       except :
          pass
        
       
       if target is None and target == '':
            target='127.0.0.1'
##       a = threading.Thread(None, self.RunPortScan, None, (target,))
##       a.start()
       self.RunPortScan(target)


    def RunPortScan(self, target=''):
        app=wx.PySimpleApp()
        title="Gomoz port scan"
        dlg=portscan.PortScanFrame(self.frame, id=-1, title=title, pos=wx.DefaultPosition, size=(400, 320)) 
        dlg.SetTarget(target)
        dlg.Center()
        dlg.Show()
        app.MainLoop()
   
    def OnShowSelecteds(self, evt):
            index = self.lc_sources.GetFirstSelected()
            if index == -1:
                 return
            while index != -1:
                item = self.lc_sources.GetItem(index)
                tab.append(item.GetText())
                index = self.lc_sources.GetNextSelected(index)
            return tab
        
    def OnRemove(self, event):
           index = self.frame.lc_sources.GetFocusedItem()
           if index ==-1:
               wx.MessageBox("Please select a row(s)!","Delete")
           else :
             index = self.frame.lc_sources.GetFirstSelected()
             while index != -1:
                self.frame.lc_sources.DeleteItem(index)
                index = self.frame.lc_sources.GetNextSelected(index)
                

    def OnRemoveAll(self, event):
        item=self.frame.lc_sources.GetItemCount()
        if item != 0:
          request="Do you really want to delete all?"
          title="Delete all"
          if wx.MessageBox(request,title,wx.ICON_QUESTION|wx.YES_NO,self.frame) == wx.YES:
             self.frame.lc_sources.DeleteAllItems()
             self.frame.r_stack=[0]
        else :
           wx.MessageBox("No data founded ...","Delete All")
          #item=self.frame.lc_sources.GetItemCount()
          #while item != 0:
              #for index in range(self.frame.lc_sources.GetItemCount()):
                   #self.frame.lc_sources.DeleteItem(index)
                   #item=self.frame.lc_sources.GetItemCount() 
    
    

