#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/tools.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:48


import time
import logging
import os
import aircv as ac
import numpy as np

from uiautomator2 import _fix_wifi_addr
from uiautomator2 import Device as Core


logger = logging.getLogger('andriodbot')

# 锁屏密码
_passwd = [(0.25, 0.611),(0.227, 0.841),(0.772, 0.864)]
_src_dir = os.path.abspath(__file__)
_src_dir = os.path.dirname(_src_dir)
_src_dir = os.path.join(_src_dir, 'src')


def platform():
    r = os.system('termux-open')
    if r == 0:
        return 'termux'


def get_bounds(elem):
    return eval(elem.attrib.get('bounds').replace('][', ','))


class Device(Core):
    def __init__(self, serial_or_url=None, detect=True, **kwargs):
        if detect:
            if platform() == 'termux':
                serial_or_url = (_fix_wifi_addr('0.0.0.0'))
        super().__init__(serial_or_url, **kwargs)
    

    def load_images(self, scr_dir=None, **kwargs):
        try:
            self.images
        except:
            self.images = {}
        scr_dir = src_dir if scr_dir else _src_dir
        for k, v in kwargs.items():
            self.images[k] = np.asarray(
                ac.imread(os.path.join(scr_dir, v))
            )


    def is_screen_on(self):
        return self.info.get('screenOn')


    def is_lock(self):
        packages = {'com.android.systemui', 'android'}
        package = self.info.get('currentPackageName')
        return package in packages 


    def unlock(self, passwd=[]):
        """
        屏幕解锁
        """
        if not self.is_screen_on():
            self.screen_on()
        # r = self(resourceId="com.android.systemui:id/qs_frame")
        # if r.wait(timeout=3):
        if self.is_lock(): 
            # nolocal _passwd
            passwd = passwd or self.settings.get("passwd") or _passwd
            self.swipe_ext("up", 0.5)
            time.sleep(0.5)
            self.swipe_points(passwd, 0.1)
        else:
            print('unlock')

    
    def window_available_info(self):
        try:
            info = self._windows_available_info
        except Exception as e:
            w, h = self.window_size()
            w0 = 10
            w -= 10
            bar = self(resourceId="com.android.systemui:id/status_bar")
            nav = self(resourceId="com.android.systemui:id/nav_buttons")
            if bar.wait(timeout=1):
                h0 = bar.bounds()[3] + 10
            else:
                h0 = 10

            if nav.wait(timeout=1):
                h = nav.bounds()[1] -10
            else:
                h = h -10
            info = self._windows_available_info = (w0, h0, w, h)
            print('初始化完成')
        return info
        

    def is_onscreen(self, r, info=None, timeout=1):
        if info is None:
           info = self.window_available_info() 
        w0, h0, w, h = info 
        if not r.wait(timeout=timeout):
            return False
        x, y = r.center()
        if y < h0 or y > h or x < w0 or x > w:
            return False
        return True

    
    def images_match(self, match, **kwargs):
        scr = np.asarray(self.screenshot())
        return ac.find_all_template(scr, match, **kwargs)


    def images_match_click(self, match, threshold=0.85, **kwargs):
        rs = self.images_match(match, threshold=threshold, **kwargs)
        print(rs, threshold)
        for i in rs:
            self.click(*i['result'])

def main():
    d = Device()
    if d.is_screen_on():
        d.screen_off()
    r = d.unlock()
    # logger.info(str(r))
    print(r)


if __name__ == "__main__":
    main()
     
