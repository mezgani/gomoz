import wx
import wx.html

class GomozBrowser(wx.Panel):
    def __init__(self, panel):
        wx.Panel.__init__(self, panel, -1)
        self.html = wx.html.HtmlWindow(self)
        if "gtk2" in wx.PlatformInfo:
            self.html.SetStandardFonts()
        #self.html.SetRelatedFrame(self, self.GetTitle() + " -- %s")
        #self.html.SetRelatedStatusBar(0)
        wx.CallAfter(self.html.LoadPage, 'http://127.0.0.1:8080/')
    

    def geturl(self, url):
        wx.CallAfter(self.html.LoadPage, url)


