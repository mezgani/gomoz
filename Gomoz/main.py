# -*- coding: utf-8 -*-

import wx
import gettext
from gui.start import *
"""Execute application"""


""" if __name__ == '__main__':"""
def main():    
    gettext.install("gomoz") 
    app = SplashApp(False)
    app.MainLoop()
