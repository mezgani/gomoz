import wx, time, os, sys, re
from xml.dom.minidom import Document
import xmlparser
import interwin, gtoolbar, about
import glistctrl, data, gstatusbar, ghelp
from ids import *

import threading
import Gomoz.gsqlite as gsqlite

class GomozMenuBar(gtoolbar.GomozToolBar, threading.Thread):
    
    def __init__(self, frame, panel, sources):
        # Initializing the toolbar object
        gtoolbar.GomozToolBar.__init__(self, frame, panel, sources)
      
        # Menu Bar
        self.frame = frame
        self.frame_menubar=wx.MenuBar()
        self.frame.SetMenuBar(self.frame_menubar)

        self.panel = panel
        self.lc_sources = sources
        self.cb_targets=''
        self.cb_proxy=''
        self.cb_exploit=''
            
    
        


        self.frame.menu_file = wx.Menu()
        self.frame.smenu_new = wx.MenuItem(self.frame.menu_file, MN_NEW, ("&New...\tCtrl-N"), "New scan", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/new_scan.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_new.SetBitmap(bmp)
        
        self.frame.menu_file.AppendItem(self.frame.smenu_new)
        self.frame.menu_file.AppendSeparator()
        self.frame.smenu_open = wx.MenuItem(self.frame.menu_file, MN_OPEN, ("&Open...\tCtrl-O"), "Open file project", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/open.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_open.SetBitmap(bmp)
        self.frame.menu_file.AppendItem(self.frame.smenu_open)
        self.frame.smenu_save = wx.MenuItem(self.frame.menu_file, MN_SAVS, ("&Save...\tCtrl-S"), "Save scan", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/save.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_save.SetBitmap(bmp)
        self.frame.menu_file.AppendItem(self.frame.smenu_save)
        self.frame.menu_file.AppendSeparator()
        self.frame.smenu_exit = wx.MenuItem(self.frame.menu_file, MN_EXIT, ("&Exit\tCtrl-Q"), "Terminate program", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/exit.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_exit.SetBitmap(bmp)
        self.frame.menu_file.AppendItem(self.frame.smenu_exit)
        self.frame_menubar.Append(self.frame.menu_file, _("&File"))


        self.frame.menu_data = wx.Menu()
        self.frame.smenu_selcsho = wx.MenuItem(self.frame.menu_data, MN_SELCSHO, ("&Scan port \tCtrl-Shift-A"),"Scan ports of selected target", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/scan_port.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_selcsho.SetBitmap(bmp)
        
        self.frame.smenu_exploit = wx.MenuItem(self.frame.menu_data, MN_EXPLOIT, ("&Exploit...\tCtrl-E"), "Load exploits from file", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/x.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_exploit.SetBitmap(bmp)
        
        self.frame.smenu_proxy   = wx.MenuItem(self.frame.menu_data, MN_PROXY, ("&Proxy...\tCtrl-P"), "Load proxies from file", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/proxy.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_proxy.SetBitmap(bmp)
        
        self.frame.smenu_target  = wx.MenuItem(self.frame.menu_data, MN_TARGET, ("&Targets...\tCtrl-T"), "Load hosts from file", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/target.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_target.SetBitmap(bmp)
        
        self.frame.menu_data.AppendItem(self.frame.smenu_target)
        self.frame.menu_data.AppendItem(self.frame.smenu_proxy)
        self.frame.menu_data.AppendItem(self.frame.smenu_exploit)
        self.frame.menu_data.AppendSeparator()
        self.frame.menu_data.AppendItem(self.frame.smenu_selcsho)
        self.frame_menubar.Append(self.frame.menu_data, ("&Data"))

        self.frame.menu_options = wx.Menu()
           
        self.frame.smenu_selcall = wx.MenuItem(self.frame.menu_options, MN_SELCALL, ("&Select  all\tCtrl-A"),"Select all", wx.ITEM_NORMAL)
        self.frame.smenu_selcnon = wx.MenuItem(self.frame.menu_options, MN_SELCNON, ("&Select None\tCtrl-Alt-A"),"Select None", wx.ITEM_NORMAL)
        self.frame.smenu_fgcolor = wx.MenuItem(self.frame.menu_options, MN_FGCOLOR, ("&Set text colour\tCtrl-Alt-T"),"Set request text colour", wx.ITEM_NORMAL)
        self.frame.smenu_bgcolor = wx.MenuItem(self.frame.menu_options, MN_BGCOLOR, ("&Set background colour\tCtrl-Alt-B"),"Set request background colour", wx.ITEM_NORMAL)
        self.frame.smenu_enedit  = wx.MenuItem(self.frame.menu_options, MN_ENEDIT,  ("&Enable request editing\tCtrl-Alt-N"),"Enable request editing", wx.ITEM_CHECK)
        self.frame.smenu_editit  = wx.MenuItem(self.frame.menu_options, MN_EDITIT,  ("&Edit current request\tCtrl-Alt-E"),"Edit current request", wx.ITEM_NORMAL)    


        self.frame.menu_options.AppendItem(self.frame.smenu_selcall)
        self.frame.menu_options.AppendItem(self.frame.smenu_selcnon)
        self.frame.menu_options.AppendSeparator()
        self.frame.menu_options.AppendItem(self.frame.smenu_fgcolor)
        self.frame.menu_options.AppendItem(self.frame.smenu_bgcolor)

        
        self.frame_menubar.Append(self.frame.menu_options, "&Options")
      
        self.frame.menu_help = wx.Menu()
        self.frame.smenu_help= wx.MenuItem(self.frame.menu_help, MN_HELP, ("&Help...\tCtrl-H"), "Help files.", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/help16.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_help.SetBitmap(bmp)
        self.frame.menu_help.AppendItem(self.frame.smenu_help)

        self.frame.menu_help.AppendSeparator()
        self.frame.smenu_about = wx.MenuItem(self.frame.menu_help, MN_ABOUT, ("&About...\tCtrl-B"), "About gomoz, securfox inc.", wx.ITEM_NORMAL)
        bmp = wx.Bitmap("Gomoz/image/aboutinfo.png", wx.BITMAP_TYPE_PNG)
        self.frame.smenu_about.SetBitmap(bmp)
        self.frame.menu_help.AppendItem(self.frame.smenu_about)
    
        self.frame_menubar.Append(self.frame.menu_help, ("&Help"))
        
        self.frame_menubar.SetBackgroundColour('white')
        self.frame_menubar.SetForegroundColour('black')
        # Menu Bar end
       
        self.__init_events()



    def __init_events(self):
 
        self.frame.Bind(wx.EVT_MENU,self.OnNewScan,   id = MN_NEW)  
        self.frame.Bind(wx.EVT_MENU,self.OnOpen,   id = MN_OPEN)  
        self.frame.Bind(wx.EVT_MENU,self.OnSavs,   id = MN_SAVS)
        self.frame.Bind(wx.EVT_MENU,self.OnExit,   id = MN_EXIT)

        self.frame.Bind(wx.EVT_MENU,self.OnExploit,id = MN_EXPLOIT)
        self.frame.Bind(wx.EVT_MENU,self.OnProxy,  id = MN_PROXY)
        self.frame.Bind(wx.EVT_MENU,self.OnTarget, id = MN_TARGET)
        self.frame.Bind(wx.EVT_MENU,self.OnScanPort, id= MN_SELCSHO)
        
        self.frame.Bind(wx.EVT_MENU,self.OnSelectAll, id= MN_SELCALL)
        self.frame.Bind(wx.EVT_MENU,self.OnSelectNone, id= MN_SELCNON)
        self.frame.Bind(wx.EVT_MENU,self.OnSetFGColour, id= MN_FGCOLOR)
        self.frame.Bind(wx.EVT_MENU,self.OnSetBGColour, id= MN_BGCOLOR)
        self.frame.Bind(wx.EVT_MENU,self.OnEnableEditing, id= MN_ENEDIT)
        self.frame.Bind(wx.EVT_MENU,self.OnEditItem, id= MN_EDITIT)

        self.frame.Bind(wx.EVT_MENU,self.OnAbout,  id = MN_ABOUT)
        self.frame.Bind(wx.EVT_MENU,self.OnHelp,  id = MN_HELP)


    def OnHelp(self, event):
        app=wx.App()
        frm = ghelp.HtmlHelp(self.frame)
        frm.OnShowHelpContents()
        app.MainLoop()
        

    def OnScanPort(self, event):
        gtoolbar.GomozToolBar.OnPortScan(self, event).start()
##       try:    
##          index=self.GetSelection()
##          if index != -1:
##              target=self.frame.lc_sources.GetItem(index, 1).GetText()
##          else:
##              target=None
##       except :
##          pass
##        
##       
##       if target is None and target == '':
##            target='127.0.0.1'
##            
##       app = wx.PySimpleApp()
##       title="Gomoz port scan"
##       dlg=portscan.PortScanFrame(self.frame, id=-1, title=title, pos=wx.DefaultPosition, size=(400, 320)) 
##       dlg.SetTarget(target)
##       dlg.Center()
##       dlg.Show()
##       app.MainLoop()


    def SetCbTarget(self, target):
        self.cb_targets=target

    def SetCbProxy(self, proxy):
        self.cb_proxy=proxy

    def SetCbExploit(self, exploit):
        self.cb_exploit=exploit




    """    def __set_combodata(self, files, mode):
        fd = open(files,'rb')
        data=fd.read()
        req=data.split('\n')
        
        for i in req:
            item=i.split('\r')
            mode.Append(item[0])
        fd.close
      	return mode.GetCount() """


    
    def OnOpen(self,event):
        title="Select file"
        wildcard = "xml files (*.xml)|*.xml |sqlite files (*.db)|*.db"

        dlg = wx.FileDialog(self.frame, title, style = wx.OPEN, wildcard=wildcard)
      	result = dlg.ShowModal()
	path = dlg.GetPath()
	if result==wx.ID_OK:
            
           if path.find('.xml') != -1:
                 filetype='xml'
           elif path.find('.XML') != -1:
                 filetype='xml'
           elif path.find('.db') != -1:
                 filetype='db'
          
           if filetype=='xml':
              try:
                if os.path.exists(path): 
                 fd = open(path, 'rb')
                 data=fd.read()
                 if data != "" or data is not None:
                    #self.frame.lc_sources.DeleteAllItems()
                    self.frame.cb_exploit.Clear()
                    self.frame.cb_targets.Clear()
                    self.frame.cb_proxy.Clear()
                    self.frame.cb_single.SetValue(0)
                    self.frame.cb_mass.SetValue(0)
                    self.frame.cb_glob.SetValue(0)
                    self.frame.tc_url.Clear()
                    l=xmlparser.XmlToDict(path)
                    self.OnInsertRows(l)
                    
                    fd.close()
              except Exception, e :
                 print e
           elif filetype=='db':
              try:
                 db=gsqlite.Gomozdblite('', '')
                 if path is not None and path != '': 
                   db.Connectdb(path)
                   data, dump=db.Selectdb()
                   dump=dump[0]
                   db.Closedb()

                   for i in range(len(data)):
                      self.frame.lc_sources.InsertStringItem(i, str(data[i][0]))
                      self.frame.lc_sources.SetStringItem(i, 1, str(data[i][1]))
                      self.frame.lc_sources.SetStringItem(i, 2, str(data[i][2]))
                      self.frame.lc_sources.SetStringItem(i, 3, str(data[i][3]))
                      self.frame.lc_sources.SetStringItem(i, 4, str(data[i][4]))

                   self.frame.cb_exploit.SetValue(str(dump[3]))
                   self.frame.cb_targets.SetValue(str(dump[0]))
                   self.frame.cb_proxy.SetValue(str(dump[2]))
                   self.frame.cb_single.SetValue(0)
                   self.frame.cb_mass.SetValue(0)
                   self.frame.cb_glob.SetValue(0)
                   self.frame.tc_url.SetValue(str(dump[1]))
         
              except Exception, msg:
                wx.MessageBox(str(msg),"Info")
               
                
	dlg.Destroy()





    def MakeTempData(self):
        path='gmz.tmp'
        try:
            
          if os.path.exists(path):
             os.remove(path)
          data=self.OnDumpMenu()
          dump=self.OnDumpData()
          db=gsqlite.Gomozdblite(dump, data)
          db.Connectdb(path)
          db.Createdb()
          db.Insertdb()
          db.Closedb()
        except Exception, msg:
          wx.MessageBox(str(msg),"Info")
          
        try:
          self.frame.lc_sources.DeleteAllItems()
          db=gsqlite.Gomozdblite('', '')
          db.Connectdb(path)
          data, dump=db.Selectdb()
          db.Closedb()
          data.sort()   
          return data
        except:
            pass


    def OnInsertRows(self,l):
        test={}

        self.frame.cb_exploit.SetValue(str(l['menu'][0]['exploit']))
        self.frame.cb_targets.SetValue(str(l['menu'][0]['url']))
        self.frame.cb_proxy.SetValue(str(l['menu'][0]['proxy']))
        self.frame.cb_single.SetValue(0)
        self.frame.cb_mass.SetValue(0)
        self.frame.cb_glob.SetValue(0)
        self.frame.tc_url.SetValue(str(l['menu'][0]['include']))

        num_items=len(l['scan'])
        for i in range(num_items):
            test=l['scan'][i]
            self.frame.lc_sources.InsertStringItem(i, str(test['request']))
            self.frame.lc_sources.SetStringItem(i, 1, str(test['url']))
            self.frame.lc_sources.SetStringItem(i, 2, str(test['exploit']))
            self.frame.lc_sources.SetStringItem(i, 3, str(test['date']))
            self.frame.lc_sources.SetStringItem(i, 4, str(test['status']))

 


    def OnSavs(self, event=None):
	
        wildcard = "xml files (*.xml)|*.xml |sqlite files (*.db)|*.db"
	title="Save File"
	dialog=wx.FileDialog(self.frame, title, style=wx.SAVE|wx.OVERWRITE_PROMPT, wildcard=wildcard)
	result = dialog.ShowModal()
	path = dialog.GetPath()
        
	
	if result==wx.ID_OK:
           try:
             if path.find('.xml') != -1:
                 filetype='xml'

             elif path.find('.db') != -1:
                 filetype='db'
             else:
                 wx.MessageBox("Format not supported","Info")
                 return
              
             if  os.path.exists(path): 
                 os.remove(path)
             if filetype=='xml':
                self.OnDumpXML(path)
             elif filetype=='db':
                self.OnDumpDB(path) 
	   except:
	     pass
	dialog.Destroy()
    

    
    def OnDumpDB(self, path):
      try:
          dump=self.OnDumpData()
          data=self.OnDumpMenu()
          db=gsqlite.Gomozdblite(dump, data)
          if path is not None and path != '': 
             db.Connectdb(path)
             db.Createdb()
             db.Insertdb()
             db.Closedb()
      except Exception, msg:
          wx.MessageBox(str(msg),"Info")



    def OnDumpTxt(self, path):
      fd = open(path, 'a')
      while 1:
        snapshot=time.strftime("%Y-%m-%d %H:%M", time.localtime())
        fd.write(snapshot + "\n")
        fd.write("scans =")
        data=self.OnDumpData()
        
        fd.write(str(data) + "\n")
        fd.write("menu =")
        data=self.OnDumpMenu()
       
        fd.write(str(data) + "\n")
        fd.write("\n")
        if input != "" or not input:
           break
      fd.close()
          

    def OnDumpXML(self, path):
      try:
          fd = open(path, 'a')
          snapshot=time.strftime("%Y-%m-%d %H:%M", time.localtime())
          
          doc = Document()
          root = doc.createElement("gomoz")
          doc.appendChild(root)
          dump=self.OnDumpData()
          data=self.OnDumpMenu()
     
          for i in dump:
              #server info 'iis|apache|others'
              scan_element = doc.createElement("scan")
              scan_element.setAttribute("request", str(i[0]))
              scan_element.setAttribute("url", str(i[1]))
              scan_element.setAttribute("exploit", str(i[2]))
              scan_element.setAttribute("date", str(i[3]))
              scan_element.setAttribute("status", str(i[4]))
              root.appendChild(scan_element)
          
          menu_element = doc.createElement("menu")
          menu_element.setAttribute("url", str(data[0]))
          menu_element.setAttribute("include", str(data[1]))
          menu_element.setAttribute("proxy", str(data[2]))
          menu_element.setAttribute("exploit", str(data[3]))
          root.appendChild(menu_element)

          xml=doc.toprettyxml()
          fd.write(xml)
          fd.close()
      except:
        pass

    def OnExploit(self,event):
        wildcard = "Text file (*.txt)|*.txt|All file (*.*)|(*.*)"
        title = "Select exploit file"
        dlg = wx.FileDialog(self.frame,title,wildcard,style = wx.OPEN)
        result = dlg.ShowModal()
	path = dlg.GetPath()
	if result==wx.ID_OK:
           self.cb_exploit.Clear()
           self.exploit_count=gtoolbar.GomozToolBar.SetCombodata(self, path, self.cb_exploit)
           if self.exploit_count > 1: 
             gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(self.exploit_count)+ " exploits loaded", 1)
           elif self.exploit_count == 1:
             gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(self.exploit_count)+ " exploit loaded", 1)               
	dlg.Destroy()
	


    def OnProxy(self,event):
        title="Select proxy file"
        wildcard = "Text file (*.txt)|*.txt|All file (*.*)|(*.*)"
        dlg = wx.FileDialog(self.frame,title, wildcard,style = wx.OPEN)
        result = dlg.ShowModal()
	path = dlg.GetPath()
	if result==wx.ID_OK:
           self.cb_proxy.Clear()
           self.proxy_count=gtoolbar.GomozToolBar.SetCombodata(self, path, self.cb_proxy)
           if self.proxy_count > 1: 
              gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(self.proxy_count)+ " proxies loaded", 1)
           elif self.proxy_count==1:
              gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(self.proxy_count)+ " proxy loaded", 1)
	dlg.Destroy()
	

    def OnTarget(self,event):
        title="Select target file"
        wildcard = "Text file (*.txt)|*.txt|All file (*.*)|(*.*)"
        dlg = wx.FileDialog(self.frame, title, wildcard, style = wx.OPEN)
	result = dlg.ShowModal()
	path = dlg.GetPath()
	if result==wx.ID_OK:
           self.cb_targets.Clear()
           self.target_count=gtoolbar.GomozToolBar.SetCombodata(self, path, self.cb_targets)
           #d=gtoolbar.GomozToolBar.GetCombodata(self, path)
           #self.cb_targets.SetValue(str(d[0]))
           if self.target_count > 1:
               gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(self.target_count)+ " targets loaded", 1)
           elif self.target_count==1:
               gstatusbar.GomozStatusBar.SetStatusText(self.frame.statusbar, str(self.target_count)+ " target loaded", 1)
               
	dlg.Destroy()


    

    def OnNewScan(self, event=None):
        gtoolbar.GomozToolBar.OnNewScan(self, event)

    def OnConfirm(self, title, msgs, event):
        msg="Do you really want to "+ msgs +" ?"
        if wx.MessageBox(msg, title, wx.ICON_QUESTION|wx.YES_NO,self.frame) == wx.YES:
            return True
        else :
            return False
 	

    def OnExit(self,event):
        if self.OnConfirm("Question","quit", event):
           self.frame.Destroy()
 	
    def OnSortAscending(self, evt):
        # recreate the listctrl with a sort style
        self.frame.lc_sources.SetSingleStyle(wx.LC_SORT_ASCENDING)
        
    def OnSortDescending(self, evt):
        # recreate the listctrl with a sort style
        self.frame.lc_sources.SetSingleStyle(wx.LC_SORT_DESCENDING)

    def OnSortByExploit(self, evt):
        def compare_func(row1, row2):
            # compare the values in the 4th col of the data
            val1 = data.row[row1][3]
            val2 = data.row[row2][3]
            if val1 < val2: return -1
            if val1 > val2: return 1
            return 0

        self.frame.lc_sources.SortItems(compare_func)
        



    def GetRowText(self, index, col):
        if index >= 0:
            return self.frame.lc_sources.GetItem(index, col).GetText()
        else:
            return ''

    def GetSelRowText(self, col):
        return self.GetRowText(self.frame.lc_sources.getSelection(), col)

    def GetSelection(self):
        return self.frame.lc_sources.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)


    def OnDumpData(self):
        rows=self.frame.lc_sources.GetItemCount()
        colums = 5
        text=[[self.GetRowText(i,j) for j in xrange(colums)]
                                      for i in xrange(rows)]
        return text

    def OnDumpMenu(self):
        snapshot=time.strftime("%Y-%m-%d %H:%M", time.localtime())
        Input = ["cb_targets", "tc_url", "cb_proxy", "cb_exploit"]
        val = [ '%s=self.frame.%s.GetValue()' % (k,k) for k in Input]
        for i in val: exec(i)
        return [cb_targets, tc_url, cb_proxy, cb_exploit]
        

    def OnDumpSelecMenu(self):        
        return [self.cb_targets_tmp, self.frame.tc_url, self.cb_proxy_tmp, self.cb_exploit_tmp]
        
        
     

    def OnShowSelected(self, evt):
        print "These items are selected:"
        index = self.frame.lc_sources.GetFirstSelected()
        if index == -1:
            print "\tNone"
            return
        while index != -1:
            item = self.frame.lc_sources.GetItem(index)
            print "\t%s" % item.GetText()
            index = self.frame.lc_sources.GetNextSelected(index)
            
    def OnSelectAll(self, evt):
        for index in range(self.frame.lc_sources.GetItemCount()):
            self.frame.lc_sources.Select(index, True)





                
    def OnSelectNone(self, evt):
        for index in range(self.frame.lc_sources.GetItemCount()):
            self.frame.lc_sources.Select(index, False)

    def OnSelectNone2(self, evt):
        index = self.frame.lc_sources.GetFirstSelected()
        while index != -1:
            self.frame.lc_sources.Select(index, False)
            index = self.frame.lc_sources.GetNextSelected(index)

    
    def OnSetFGColour(self, evt):
        index = self.frame.lc_sources.GetFocusedItem()
        if index ==-1:
            wx.MessageBox("Please select a row(s) !","Info")
        else :
           dlg = wx.ColourDialog(self.frame)
           if dlg.ShowModal() == wx.ID_OK:
              colour = dlg.GetColourData().GetColour()
              index = self.frame.lc_sources.GetFirstSelected()
              while index != -1:
                self.frame.lc_sources.SetItemTextColour(index, colour)
                index = self.frame.lc_sources.GetNextSelected(index)
           dlg.Destroy()

    def OnSetBGColour(self, evt):
        index = self.frame.lc_sources.GetFocusedItem()
        if index ==-1:
            wx.MessageBox("Please select a row(s) !","Info")
        else :
      
           dlg = wx.ColourDialog(self.frame)
           if dlg.ShowModal() == wx.ID_OK:
             colour = dlg.GetColourData().GetColour()
             index = self.frame.lc_sources.GetFirstSelected()
             while index != -1:
                self.lc_sources.SetItemBackgroundColour(index, colour)
                index = self.frame.lc_sources.GetNextSelected(index)
           dlg.Destroy()


    def OnEnableEditing(self, evt):
        self.editable = evt.IsChecked()
        
        import interwin
        #self.frame.checklister=glistctrl.CheckListCtrl(self.frame, self.frame.notebook_panel_scan, self.frame.lc_sources)
        #interwin.InterGomoz.__do_layout()
        self.MakeTempData()

        
    def OnEditItem(self, evt):
        index = self.frame.lc_sources.GetFirstSelected()
        if index != -1:
            self.frame.lc_sources.EditLabel(index)


	    
		
    def OnClear(self, event=None):
	self.cb_targets.Clear()
	self.cb_proxy.Clear()
	self.cb_exploit.Clear()

    def OnAbout(self, event):
        #self.OnDumpData()
        #self.OnDumpSelecMenu()
        dlg=about.AboutDialog(self.frame, -1, 'About dialog box')
        dlg.OnAboutBox(event=None)
        dlg.Destroy()


	








