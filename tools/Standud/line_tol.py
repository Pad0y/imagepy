# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from core.roi import lineroi
import wx
from core.engines import Tool

class Linebuf:
    def __init__(self):
        self.buf = []
        
    def addpoint(self, p):
        self.buf.append(p)
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen((0,255,255), width=1, style=wx.SOLID))
        dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCirclePoint(f(*i),2)
    
    def pop(self):
        a = self.buf
        self.buf = []
        return a
        
from core.engines import Tool

class Plugin(Tool):
    title = 'Line'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.helper = Linebuf()
        self.odx,self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        ips.mark = self.helper
        if btn==1:
            # 如果有没有在绘制中，且已经有roi，则试图选取
            if not self.doing:
                if ips.roi!= None:
                    self.curobj = ips.roi.pick(x, y)
                if self.curobj!=None:return
                    
                if ips.roi == None:
                    ips.roi = lineroi.LineRoi()
                    self.doing = True
                elif ips.roi.dtype=='line' and key['shift']:
                    self.doing = True
                else: ips.roi = None
            if self.doing:
                self.helper.addpoint((x,y))
                self.curobj = (self.helper.buf, -1)
                self.odx, self.ody = x,y
            
        elif btn==3:
            if self.doing:
                self.helper.addpoint((x,y))
                self.doing = False
                ips.roi.addline(self.helper.pop())
        ips.update = True
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.curpts = None
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.roi.snap(x, y)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.roi.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update = True
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass