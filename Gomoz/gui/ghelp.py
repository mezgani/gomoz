import wx
import wx.html

class HtmlHelp(wx.Frame):
    def __init__(self, parent):
        self.InitHelp()

        
    def InitHelp(self):
        def _addBook(filename):
            if not self.help.AddBook(filename):
                wx.MessageBox("Unable to open: " + filename,
                              "Error", wx.OK|wx.ICON_EXCLAMATION)

        self.help = wx.html.HtmlHelpController()

        _addBook("Gomoz/helpfiles/testing.hhp")
        _addBook("Gomoz/helpfiles/another.hhp")


    def OnShowHelpContents(self):
        self.help.DisplayContents()

    def OnShowHelpIndex(self, evt):
        self.help.DisplayIndex()

    def OnShowSpecificHelp(self, evt):
        self.help.Display("sub book")


