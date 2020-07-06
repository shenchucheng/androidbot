#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import os
import sys
import time


from .tools import Device, get_bounds, logger


# 识别图片字典
images_dict = {
    'hand':  'hand.jpg',
    'heart': 'heart.jpg',
    'help':  'help.jpg',
    'help2': 'help1.jpg',
    'gain':  'gain.jpg'
    }


def noexists_raise(timeout=1):
    while 1:
        if r.wait(timeout=timeout):
            tries = 0
            return True
        else:
            if tries >= max_tries:
                raise
            tries += 1

      
def get_next_time(self):
    pass


def energy_friend_locate(self):
    pass


# 获取好友列表
def friends_list(self):
    r = self(text='没有更多了')
    for i in range(20):
        if r.wait(timeout=1):
            break
        else:
            self.swipe_ext('up', 0.75)

    r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]')
    r.wait()
    elem = r.elem.getchildren()
    i = 1
    l = []
    for _ in elem:
        r = energy_friends_info(_, i)
        i = r[0] + 1
        l.append(r)
    return l


def energy_friends_info(friend, i):
    c = friend.getchildren()
    c1 = c[0].getchildren()
    if c1:
        c1 = c1[0].get('text')
        if c1:
            i = c1 = int(c1)
        else:
            c1 = i
    else:
        c1 = i
    c2 = c[2].getchildren()[0].getchildren()[0].get('text')
    c3 = c[4].getchildren()
    if c3:
        c3 = c3[0].get('text').strip('’')
        c3 = int(c3)
    else:
        c3 = -1
    return (c1, c2, c3)


# 获取当前可视范围
def energy_friends_current(self, first=False, num=False):
    r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]')
    r.wait()
    elem = r.elem.getchildren()
    e0 = elem[0]
    p0 = get_bounds(e0)
    if first:
        return (energy_friends_info(e0, 1), p0)
    l = []
    i = 2
    t1 = t2 = 0
    for e in elem[1:-1]:
        p = get_bounds(e)
        c1, c2 = (p[1]-p0[1], p[3]-p0[3])
        if c1 > 0:
            t1 += 1
        if c2 > 0:
            t2 += 1
        if all((c1>0, c2>0)):
            l.append((energy_friends_info(e, i), p))
        i += 1
        (e0, p0) = (e, p)
    if num:
        return round((l[0][0][0]+l[-1][0][0])/2)
    return l  


# 识别手势与爱心
def energy_page(self, plus=False, threshold=0.9, timeout=5, **kwargs):
    r = self(text='总排行榜')
    r.wait(timeout=timeout)
    rs = self.images_match(self.images['hand'], threshold=threshold, **kwargs)
    for i in rs:
        self.click(*i['result'])
        energy_gain(self)
        r.wait(timeout=timeout)
    # screenshot self.click(*i['result'])t = np.asarray(self.screenshot())
    # rs = ac.find_all_template(screenshot, self.images['hand'], threshold=threshold)
    if plus:
        for p in ['help', 'help1']:
            for i in self.images_match(self.images[p], threshold=threshold, **kwargs):
                rs.append(i)
                self.click(*i['result'])
                energy_gain(self, threshold=0.7, timeout=1)
                r.wait(timeout=timeout)
    return rs


def energy_gain(self, timeout=3, threshold=0.8, **kwargs):
    # self.images_match_click(self.images['gain'], threshold=threshold, **kwargs)
    # gain
    r = self(textContains='收集能量')
    if r.wait(timeout=timeout):
        p0 = r.center()
        r.click()
        while 1:
            time.sleep(0.3)
            if r.wait(timeout=1):
                p = r.center()
                if p == p0:
                    break
                p0 = p
                r.click()
            else:
                break
    else:
        if self(text='总排行榜').wait(timeout=1):
            return

    self.images_match_click(self.images['help'], threshold=threshold) 
    self.press('back')


# 翻页
def energy_next_page(self):
    self.swipe_ext('up', 0.5)
     
        
def energy_friends(self, timeout=1, max_tries=5):
    tries = 0
    r = self(text='查看更多好友')
    # noexists_raise()
    while not self.is_onscreen(r):
        if tries >= max_tries:
            raise
        tries += 1
        self.swipe_ext('up', 0.6)
    r.click()


def energy_self_love(self, timeout=3):
    r = self(text=" ")
    t = 0
    while r.click_exists(timeout=timeout):
        t += 1
    return t


def energy_self(self, max_tries=10):
    # energy_self_love(self)
    tries = 1
    while 1:
        r = self(textContains='收集能量')
        if r.click_exists(timeout=10):
            tries = 0
        else:
            if not tries:
                break
            elif tries < max_tries:
                tries += 1
                self.click(0,0)
                print(tries)
            else:
                break


def energy_love(self):
    r = self(text='合种')
    r.click_exists(timeout=5)
    r = self.xpath('//*[@resource-id="J-dom"]/android.view.View[1]/android.view.View[6]/android.view.View[1]/android.view.View[1]')
    r.click_exists(timeout=5)
    r = self(text='浇水')
    if r.wait(timeout=3):
        r.click()
    else:
        if self(text='在该合种浇水已达上限，明天继续哟').wait(timeout=1):
            pass
        self(text='知道了').click()

    for i in range(1, 3):
        r = self.xpath('//android.widget.ListView/android.view.View[{}]'.format(i))
        r.click()
        r = self(text='浇水')
        if r.wait(timeout=4):
            break
        else:
            self.press('back')

    for _ in range(3):
        for i in ['浇水', '66克', '浇水送祝福']:
            self(text=i).click_exists(timeout=3)
    self.press('back')
    self.press('back')


def alipay_energy(self, mode=0, plus=0):
    self.alipay_start()
    r = self(text='蚂蚁森林')
    if not r.wait(timeout=3):
        self.alipay_start(init=1)
    r.click()
    if mode in [1, 3, 5, 7]:
        energy_self(self)
        if mode == 1:
            self.press('back')
            self.press('home')
            self.screen_off()
            return

    if mode in [2, 3, 6, 7]:
        energy_love(self)
        if mode == 2:
            self.press('back')
            self.press('home')
            self.screen_off()
            return
        
    if mode == 3:
        return

    energy_friends(self)
    time.sleep(0.5)
    self(text='总排行榜').click()
    r2 = self(text='没有更多了')
    while not self.is_onscreen(r2):
        energy_page(self, plus=plus)
        energy_next_page(self)
    self.press('back')
    self.press('back')
    self.press('home')
    self.screen_off()
   

def alipay_start(self, init=False, max_tries=4):
    package='com.eg.android.AlipayGphone'
    self.unlock()
    if init:
        self.session(package)
        self.app_wait(package)
    else:
        self.app_start(package)
        self.app_wait(package)
        r = self(resourceId='com.alipay.android.phone.openplatform:id/tab_description')
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

def load(self):
    self.alipay_start = alipay_start
    self.alipay_energy = alipay_energy
    self.images = {}
    self.load_images(self, **images_dict)


def main():
    args = sys.argv
    d = Device()
    kwargs = {}
    mode = 0
    if '--plus' in args:
        kwargs['plus'] = 1

    if '--self' in args:
        mode += 1

    if '--love' in args:
        mode += 2

    if '--friends' in args:
        mode += 4

    kwargs['mode'] = mode
    d.alipay_energy(**kwargs)


load(Device)

if __name__ == '__main__':
    main()

