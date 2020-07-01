#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import os
import sys
import time


from .tools import Device, unlock, termux_local_connect, logger


def alipay_start(self, package='com.eg.android.AlipayGphone', init=False, max_tries=4):
    self.unlock()
    if init:
        self.session(package)
        self.app_wait(package)
    else:
        self.app_start(package)
        self.app_wait(package)
        r = self(resourceId="com.alipay.android.phone.openplatform:id/tab_description")
        while 1:
            if max_tries <= 0:
                self.alipay_start(init=True)
                break
            elif r.wait(timeout=1):
                r.click()
                break
            else:
                self.press('back')
                max_tries -= 1


def alipay_energy(self, mode=2, start=1, end=90, max_tries=10, exclude=[],
        recircle=False, max_time=1500, start_time=0):
    start_time = start_time or time.time()
    if recircle < 2:
        self.alipay_start()
        self(text="蚂蚁森林").click()

    # 收取自己的能量
    if mode == 0:
        tries = 1
        while 1:
            r = self(textContains="收集能量")
            if r.wait(timeout=10):
                text = r.get_text()
                r.click()
                logger.info("自己：{}".format(text))
                tries = 0
            else:
                if not tries:
                    break
                elif tries < 10:
                    tries += 1
                    print(tries)
                else:
                    break
        self.screen_off()
        return

    elif mode == 1:
        r = self(text='合种')
        r.click_exists(timeout=5)
        r = self.xpath('//*[@resource-id="J-dom"]/android.view.View[1]/android.view.View[6]/android.view.View[1]/android.view.View[1]')
        r.click_exists(timeout=5)
        r = self(text="浇水")
        if r.wait(timeout=3):
            r.click()
        else:
            if self(text='在该合种浇水已达上限，明天继续哟').wait(timeout=1):
                pass
            self(text='知道了').click()
        r = self(text='今日排行')
        if r.wait(timeout=5):
            r.click()
        r =self(text='颖灵')
        if r.wait(timeout=5):
            r.left().click_exists(timeout=3)
        for _ in range(3):
            for i in ['浇水', '66克', '浇水送祝福']:
                self(text=i).click_exists(timeout=3)
        self.alipay_home()
        self.alipay_back()
        self.alipay_back()
        self.screen_off()
        return


    # 查看所有好友，待改善
    first = recircle < 2
    r = self(text="查看更多好友")
    while first:
        if r.wait(timeout=5):
            self.swipe_ext('up',0.8)
            time.sleep(0.5)
            self.swipe_ext('up', 0.5)
            r.click()
            self.app_wait("com.eg.android.AlipayGphone")
            # 获取自己的排名
            r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[1]/android.view.View[1]')

            r.wait()
            elem = r.elem.getchildren()
            num = elem[0].getchildren()
            if num:
                num = num[0].get('text')
                num = int(num)
            else:
                user = elem[2].getchildren()[0].getchildren()[0].get('text')
                for i in [1, 2]:
                    r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]/android.view.View[{}]'.format(i))
                    r.wait()
                    elem = r.elem.getchildren()
                    if elem[2].getchildren()[0].getchildren()[0].get('text') == user:
                        num = i
                num = num if num else 3
            logger.info('我的排名:' + str(num))
            exclude.append(num)
            break
        else:
            time.sleep(2)
    i = start
    tries = 0
    while 1:
        if time.time() - start_time > max_time:
            self.screen_off()
            return
        if i in exclude:
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
            if p < 0.9 and not r.elem.getchildren(): 
                # 等待收取时，time_info = r.elem.getchildren() 子节点列表
                # 此时包含列表首值 time_info.getchildren().get('text')
                # 返回成熟等待时间 11'
                r.click()
                self.app_wait("com.eg.android.AlipayGphone")
                r = self(textContains="收集能量")
                if r.wait(timeout=2):
                    for _ in r:
                        r.click_exists(timeout=1)
                        time.sleep(0.3)
                    exclude.append(i)
                else:
                    r = self(text='\xa0')
                    r.click_exists()
                self.press('back')

            if i < end:
                i += 1
            else:
                break
            self.swipe_ext("up", 0.05)
            tries = 0
        else:
            exclude.append(i)
            self.swipe_ext("up", 0.4)
            tries += 1
    
    if recircle:
        if end - start - len(exclude) > 5:
            for i in range(5):
                self.swipe_ext('down', 0.7)
                time.sleep(0.1)
            recircle += 1
            self.alipay_energy(start=start, end=end, exclude=exclude,
                        mode=mode, recircle=recircle, max_time=max_time,
                        start_time=start_time, max_tries=10)
        else:
            self.screen_off()
    else:
        self.screen_off()
    

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
    argv = sys.argv
    mode = 0 if  '--self' in argv else 1 if '--love' in argv else 2
    recircle = True if '--recircle' in argv else False
    d.alipay_energy(mode=mode, recircle=recircle)


load(Device)
if __name__ == "__main__":
    main()
     
