# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 21:29:59 2016

@author: yxl
"""

import wx
from polygonroi import PolygonRoi
from core.draw import paint
from roi import ROI

class RectangleRoi(ROI):
    dtype = 'rect'
    def __init__(self, l=0, t=0, r=0, b=0):
        self.body = []
        self.update = False
        self.lt, self.tp, self.rt, self.bm = l, t, r, b
        self.commit()
    
    def snap(self, x, y):
        if abs(x-self.lt)<3 and abs(y-(self.tp+self.bm)/2)<3:return 'l'
        if abs(x-self.rt)<3 and abs(y-(self.tp+self.bm)/2)<3:return 'r'
        if abs(x-(self.lt+self.rt)/2)<3 and abs(y-self.tp)<3:return 't'
        if abs(x-(self.lt+self.rt)/2)<3 and abs(y-self.bm)<3:return 'b'
        if abs(x-self.lt)<3 and abs(y-self.tp)<3:return 'lt'
        if abs(x-self.rt)<3 and abs(y-self.bm)<3:return 'rb'
        if abs(x-self.rt)<3 and abs(y-self.tp)<3:return 'rt'
        if abs(x-self.lt)<3 and abs(y-self.bm)<3:return 'lb'
        return None
    
    def commit(self):
        l,r,t,b = self.lt, self.rt, self.tp, self.bm
        self.update = True
        if l==r or t==b: 
            self.body = [];return False
        else: 
            self.body = [(l,b),(r,b),(r,t),(l,t),(l,b)]
            return True
        
    def pick(self, x, y):
        rst = self.snap(x,y)
        if rst != None:return rst
        if (x-self.lt)*(x-self.rt)<0 and (y-self.tp)*(y-self.bm)<0:
            return True
        return None

    def draged(self, ox, oy, nx, ny, i):
        if i == True:
            self.lt, self.rt = self.lt+nx-ox, self.rt+nx-ox
            self.tp, self.bm = self.tp+ny-oy, self.bm+ny-oy
        else:
            if 'l' in i:self.lt = nx
            if 'r' in i:self.rt = nx
            if 't' in i:self.tp = ny
            if 'b' in i:self.bm = ny
        self.commit()
        
    def get_box(self):
        return [self.lt, self.tp, self.rt, self.bm]
        
    def topolygon(self):
        pg = PolygonRoi()
        pg.body.append([self.body, []])
        return pg
        
    def affine(self, m, o):
        return self.topolygon().affine(m,o)
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        dc.DrawLines([f(*i) for i in self.body])
        for i in self.body:dc.DrawCirclePoint(f(*i),2)
        dc.DrawCirclePoint(f(self.lt, (self.tp+self.bm)/2),2)
        dc.DrawCirclePoint(f(self.rt, (self.tp+self.bm)/2),2)
        dc.DrawCirclePoint(f((self.lt+self.rt)/2, self.tp),2)
        dc.DrawCirclePoint(f((self.lt+self.rt)/2, self.bm),2)
        
    def sketch(self, img, w=1, color=None):
        pen = paint.Paint()
        xs, ys = [x[0] for x in self.body], [x[1] for x in self.body]
        pen.draw_path(img, xs, ys, w, color)
        
    def fill(self, img, color=None):
        pen = paint.Paint()
        for i in self.body:
            pen.fill_polygon(self.body, img, [], color)