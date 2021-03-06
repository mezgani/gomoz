import wx
import path

class AboutDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, -1, title ,size=(400, 260) )
    def OnAboutBox(self, event):
        description  = """Gomoz is an open source Web Application Security\nScanner developed by Native LABS.\n"""
        description += """Gomoz will test a web server in the shortest \ntimespan possible, and produce deeply a pen test intrusion."""
        description += """\nGomoz is free software; you can redistribute it\nand/or modify it under the terms of the GNU"""
        description += """\nGeneral Public License as published by\nthe Free Software Foundation; either version 2 """
        description += """\nof the License, or (at your option) any later version.\nSee the GNU General Public License for more details. """


        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon(path.directory()+'/Gomoz/image/gomoz1.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Gomoz !')
        info.SetVersion('1.0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2006 Native LABS')
        info.SetWebSite('http://www.nativelabs.org/')
        info.AddDeveloper('MEZGANI Ali \nmezgani@nativelabs.org')

        wx.AboutBox(info)
