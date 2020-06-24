#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import uiautomator2

from functools import partial


from .tools import unlock


def start_alipay(self):
    self.unlock()
    self.app_start("com.eg.android.AlipayGphone")
    self.app_wait("com.eg.android.AlipayGphone")
    self.ali_home()
    self(resourceId="com.alipay.android.phone.openplatform:id/tab_description").click()
    self.app_wait("com.eg.android.AlipayGphone")


def energy_friend(self, start=0, end=90, max_tries=10):
    self.start_alipay()
    self(text="蚂蚁森林").click()
    while 1:
        r = self(text="查看更多好友")
        if r.exists:
            self.swipe_ext('up',0.9)
            r.click()
            break
        else:
            time.sleep(2)
    self.app_wait("com.eg.android.AlipayGphone")
    tries = 0
    i = start
    while 1:
        r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]/android.view.View[{}]'.format(i))
        if r.exists(timeout=3):
            r.click()
            self.app_wait("com.eg.android.AlipayGphone")
        while 1:
            r   = d(textContains="收集能量")
            if r.exists(timeout=3):
                r.click()
                time.sleep(0.5)
            else:
                break
        self.ali_back()
        if i < end:
            i += 1
        else:
            break
        self.swipe_ext("up", 0.05)
        tries = 0
    else:
        self.swipe_ext("up", 0.05)
        tries += 1
    


def ali_back(self):
    r = self(resourceId="com.alipay.mobile.nebula:id/h5_nav_back")
    if r.exists:
        r.click()
        self.app_wait("com.eg.android.AlipayGphone")

def ali_home(self):
    r = self(text="")
    # r = self.xpath('//*[@resource-id="com.alipay.mobile.nebula:id/h5_nav_options"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[2]')
    if r.exists:
        r.click()
        self.app_wait("com.eg.android.AlipayGphone")


def main():
    d = uiautomator2.connect()
    d.start_alipay  = partial(start_alipay,  self=d)
    d.ali_back      = partial(ali_back,      self=d)
    d.ali_home      = partial(ali_home,      self=d)
    d.energy_friend = partial(energy_friend, self=d)
    d.energy_friend()


if __name__ == "__main__":
    main()
     
