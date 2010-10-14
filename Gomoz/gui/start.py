import wx, interwin, time


class SplashApp(wx.App):

    def OnInit(self):
        self.count=0
        """for i in range(11,34):
            req1="bmp = wx.Image(\"Gomoz/image/splash%s.png\").ConvertToBitmap()" % i 
            req2="self.spl%s=wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,4000, None, -1)" % i
            exec(req1)
            exec(req2)
            #time.sleep(0.2)
            """
            
            #this="self.gauge%s = wx.Gauge(self.spl%s, -1, 100, (0, 264), (400, 25))" % (i,i)
            #exec(this)
            
            #face="self.gauge%s.SetBezelFace(3)" % i
            #shadow="self.gauge%s.SetShadowWidth(3)" % i
            #exec(face)
            #exec(shadow)
            #self.Bind(wx.EVT_IDLE, self.OnIdle)
            #self.count = self.count + 5
            #req="self.gauge%s.SetValue(self.count)" % i
            #exec(req)
            #time.sleep(1.2)




        wx.Yield()

        frame = interwin.InterGomoz(None, -1, "")
        frame.SetSize((900,550))
        frame.SetPosition((100,100))
        frame.Show(True)
        frame.SetBackgroundColour('black')
        self.SetTopWindow(frame)
        frame.Show()
        return True

      

