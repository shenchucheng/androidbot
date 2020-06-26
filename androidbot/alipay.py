#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import time
from functools import partial

from .tools import Device, unlock, termux_local_connect, logger


def alipay_start(self):
    self.unlock()
    self.app_start("com.eg.android.AlipayGphone")
    self.app_wait("com.eg.android.AlipayGphone")
    self.alipay_home()
    self(resourceId="com.alipay.android.phone.openplatform:id/tab_description").click()
    self.app_wait("com.eg.android.AlipayGphone")


def alipay_energy(self, mode=1, start=1, end=90, max_tries=10):
    self.alipay_start()
    self(text="蚂蚁森林").click()

    # 收取自己的能量
    while 1:
        r = self(textContains="收集能量")
        if r.wait(timeout=3):
            text = r.get_text()
            r.click()
            logger.info("自己：{}".format(text))
        else:
            break
    if mode == 0:
        return
    
    # 查看所有好友，待改善
    while 1:
        r = self(text="查看更多好友")
        if r.exists:
            self.swipe_ext('up',0.9)
            r.click()
            self.app_wait("com.eg.android.AlipayGphone")
            break
        else:
            time.sleep(2)

    # 获取自己的排名
    r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]')
    if r.wait(timeout=5):
        num = int(r.get_text())
    else:
        raise

    tries = 0
    i = start
    while 1:
        if i == num:
            i += 1
            continue
        r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]/android.view.View[{}]/android.view.View[5]'.format(i))
        if r.wait(timeout=3):
            p = r.screenshot()
            p = p.convert('L')
            b = l = 0
            for c in p.getdata():
                l += 1
                if c > 240:
                    b += 1
            p = b/l  # 空白率
            print(p)
            if p < 0.9:    
                r.click()
                self.app_wait("com.eg.android.AlipayGphone")
                while 1:
                    r = self(textContains="收集能量")
                    if r.wait(timeout=2):
                        r.click()
                        time.sleep(0.5)
                    else:
                        break
                r = self(text='\xa0')
                r.click_exists()
                self.alipay_back()


            if i < end:
                i += 1
            else:
                break
            self.swipe_ext("up", 0.05)
            tries = 0
        else:
            self.swipe_ext("up", 0.5)
            tries += 1
    


def alipay_back(self):
    r = self(resourceId="com.alipay.mobile.nebula:id/h5_nav_back")
    if r.exists:
        r.click()
        self.app_wait("com.eg.android.AlipayGphone")


def alipay_home(self):
    r = self(text="")
    # r = self.xpath('//*[@resource-id="com.alipay.mobile.nebula:id/h5_nav_options"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[2]')
    if r.exists:
        r.click()
        self.app_wait("com.eg.android.AlipayGphone")


def load(self):
    self.alipay_start  = alipay_start
    self.alipay_home   = alipay_home
    self.alipay_back   = alipay_back
    self.alipay_energy = alipay_energy
    

def main():
    d = termux_local_connect(Device) or Device()
    d.alipay_energy()

load(Device)
if __name__ == "__main__":
    main()
     
