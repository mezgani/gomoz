import wx
import time
import threading
import Gomoz.scan.scan as scan
import path

class PortScanFrame(wx.Frame,threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        wx.Frame.__init__(self, *args, **kwargs)
        self.setDaemon (1)
        self.start()
        
        #self.start = False
        self.panel = wx.Panel(self, -1, size=(400, 320))
        ico=path.directory()+"/Gomoz/image/scf.ico"
        self.icon = wx.Icon(ico, wx.BITMAP_TYPE_ICO) 
        self.SetIcon(self.icon) 

        self.data= []

    
          
       
        #self.panel.SetBackgroundColour('black')
        self.label  = wx.StaticText(self.panel, -1, "Target(s):", pos=(50,30))
        #self.label.SetForegroundColour('yellow')
        self.input  = wx.TextCtrl(self.panel, -1, "127.0.0.1", size=(238,20),pos=(110,30))

        self.label  = wx.StaticText(self.panel, -1, "start port :", pos=(50,55))
        #self.label.SetForegroundColour('yellow')
        
        self.label  = wx.StaticText(self.panel, -1, "end port :", pos=(230,55))
        #self.label.SetForegroundColour('yellow')
        
        self.startport = wx.SpinCtrl(self.panel, -1, "", (287, 55), (60, -1))
        self.startport.SetRange(1,65535)
        self.startport.SetValue(80)

        self.endport = wx.SpinCtrl(self.panel, -1, "", (110, 55), (60, -1))
        self.endport.SetRange(1,65535)
        self.endport.SetValue(80)
        
	
      
        self.input.SetBackgroundColour('black')
        self.input.SetForegroundColour('blue')

        

        self.button1 = wx.Button(self.panel, id=-1, pos=(242, 250))
        self.button1.SetLabel('Start')
        #self.button1.SetBackgroundColour('black')
        #self.button1.SetForegroundColour('green')
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton)

        self.button2 = wx.Button(self.panel, id=-1, pos=(100, 250))
        self.button2.SetLabel('Clear')
        #self.button2.SetBackgroundColour('black')
        #self.button2.SetForegroundColour('green')
        self.button2.Bind(wx.EVT_BUTTON, self.OnClear)

        self.__initialize__()
        self.Set_events_()
        



    def __initialize__(self):
        il = wx.ImageList(16,16)
        self.fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.fldropenidx = il.Add( wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, (16,16)))
        self.fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16,16)))
        self.tree = wx.TreeCtrl(self.panel,size=(300,140),pos=(50,85))
        self.tree.SetBackgroundColour('black')
        self.tree.SetForegroundColour('green')
        self.tree.AssignImageList(il)
        root = self.tree.AddRoot("localhost")
        self.tree.SetItemImage(root, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.SetItemPyData(root, self.data)
        self.tree.SetItemHasChildren(root, True)
        self.tree.Expand(root)

    def Set_events_(self):   
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, self.tree)



    def SetTarget(self, host):
        if host is  None or host.strip() =='':
            host="127.0.0.1"
        else:    
            self.input.SetValue(host)

    def AddTreeNodes(self, parentItem):
        """
        Add nodes for just the children of the parentItem
        """
        items = self.tree.GetItemPyData(parentItem)
        for item in items:
            if type(item) == str:
                # a leaf node
                newItem = self.tree.AppendItem(parentItem, item)
                self.tree.SetItemImage(newItem, self.fileidx,
                                       wx.TreeItemIcon_Normal)
            else:
                # this item has children
                newItem = self.tree.AppendItem(parentItem, item[0])
                self.tree.SetItemImage(newItem, self.fldridx,
                                       wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(newItem, self.fldropenidx,
                                       wx.TreeItemIcon_Expanded)
                self.tree.SetItemPyData(newItem, item[1])
                self.tree.SetItemHasChildren(newItem, True)
   
                

    def GetItemText(self, item):
        if item:
            return self.tree.GetItemText(item)
        else:
            return ""
        
    def OnItemExpanded(self, evt):
        print "OnItemExpanded: ", self.GetItemText(evt.GetItem())

    def OnItemExpanding(self, evt):
        # When the item is about to be expanded add the first level of child nodes
        print "OnItemExpanding:", self.GetItemText(evt.GetItem())
        self.AddTreeNodes(evt.GetItem())
        
    def OnItemCollapsed(self, evt):
        print "OnItemCollapsed:", self.GetItemText(evt.GetItem())
        # And remove them when collapsed as we don't need them any longer
        self.tree.DeleteChildren(evt.GetItem())

    def OnSelChanged(self, evt):
        print "OnSelChanged:   ", self.GetItemText(evt.GetItem())

    def OnActivated(self, evt):
        print "OnActivated:    ", self.GetItemText(evt.GetItem())



    def GetPorts(self):
        if self.startport.GetValue() > self.endport.GetValue():
            startport = self.endport.GetValue()
            endport   = self.startport.GetValue()     
        elif self.startport.GetValue() < self.endport.GetValue():
            endport = self.endport.GetValue()
            startport = self.startport.GetValue()
        elif self.startport.GetValue() == self.endport.GetValue():
            startport, endport = self.endport.GetValue(), self.endport.GetValue()
        return (startport, endport)


    def OnButton(self, event=None):
        host=self.input.GetValue()
        self.start=True
        start, end = self.GetPorts()
        if start==end:
            print host +" scan port "+ str(start) + "\n"
        else:    
            print host +" scan from "+ str(start) + " to "+ str(end) + "\n"
        chrono = time.time()
        result=scan.scan(host, start, end, 300)
        ports = [key for key in result.keys()]
        ports.sort()
        ports = [str(key)+" "+str("open") for key in ports]
        self.data, tab=[], []
        tab.append(host)
        tab.append(ports)
        self.data.append(tab)
        self.OnRestart()
        chrono = time.time() - chrono
        chrono = str(chrono)[:5]
        wx.MessageBox("scan finished in "+chrono+"s.","Info")



    def OnClear(self,evt):
        self.data=[]
        self.OnRestart()

    def OnRestart(self):
        self.tree.Destroy()
        self.__initialize__()
        self.Set_events_()
        self.Refresh()

    
    def OnExit(self, evt):
        self.Close()




