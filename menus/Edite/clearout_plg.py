# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 11:20:19 2016

@author: yxl
"""

from core.engines import Filter
from core.managers import ColorManager

class Plugin(Filter):
    title = 'Clear Out'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    #process
    def run(self, ips, img, buf, para=None):
        buf[ips.get_msk('out')] = ColorManager.get_back(img.ndim==2)