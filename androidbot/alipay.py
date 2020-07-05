#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import os
import sys
import time


from .tools import Device, get_bounds, logger


images_dict = {
    'hand': 'hand.jpg',
    'heart': 'heart.jpg',
    'help': 'help.jpg',
    'gain': 'gain.jpg'
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
    r = self(text="没有更多了")
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
        for i in self.images_match(self.images['heart'], threshold=threshold, **kwargs):
            rs.append(i)
            self.click(*i['result'])
            energy_gain(self, threshold=0.75, timeout=1)
            r.wait(timeout=timeout)
    return rs


def energy_gain(self, timeout=3, threshold=0.8, **kwargs):
    # self.images_match_click(self.images['gain'], threshold=threshold, **kwargs)
    # gain
    r = self(textContains='收集能量')
    if r.wait(timeout=timeout):
        r.click()
        while 1:
            time.sleep(0.3)
            if r.wait(timeout=1):
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
    r = self(text="查看更多好友")
    # noexists_raise()
    while not self.is_onscreen(r):
        if tries >= max_tries:
            raise
        tries += 1
        self.swipe_ext('up', 0.6)
    r.click()


def energy_self(self, max_tries=10):
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
            elif tries < max_tries:
                tries += 1
                print(tries)
            else:
                break


def energy_love(self):
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

def load(self):
    self.alipay_start = alipay_start
    self.alipay_energy = alipay_energy
    self.images = {}
    self.load_images(self, **images_dict)


# def alipay_energy(self, mode=2, start=1, end=90, max_tries=10, exclude=[],
#         recircle=False, max_time=1500, start_time=0):
#     
#     # 进入蚂蚁森林
#     if recircle < 2:
#         self.alipay_start()
#         self(text="蚂蚁森林").click()
#     start_time = start_time or time.time()
#     tries = 0
# 
#     # 收取自己的能量
#     if mode == 0:
# 
#     elif mode == 1:
#     def noexists_raise(timeout=1):
#         while 1:
#             if r.wait(timeout=timeout):
#                 tries = 0
#                     return True
#                 else:
#                     if tries >= max_tries:
#                         raise
#                     tries += 1
#                     
#     def __friends(recircle):
#         first = recircle < 2
#         if first:
#             r = self(text="查看更多好友")
#             # noexists_raise()
#             while 1:
#                 if self.is_onscreen(r):
#                     r.click()
#                     tries = 0
#                     break
#                 else:
#                     if tries >= max_tries:
#                         raise
#                     tries += 1
#                     self.swipe_ext('up', 0.5)
# 
#             # 获取自己排名
#             r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[1]/android.view.View[1]')
# 
#             # r.wait()
#             elem = r.elem.getchildren()
#             num = elem[0].getchildren()
#             if num:
#                 num = num[0].get('text')
#                 num = int(num)
#             else:
#                 user = elem[2].getchildren()[0].getchildren()[0].get('text')
#                 for i in [1, 2]:
#                     r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]/android.view.View[{}]'.format(i))
#                     # r.wait()
#                     elem = r.elem.getchildren()
#                     if elem[2].getchildren()[0].getchildren()[0].get('text') == user:
#                         num = i
#                 num = num if num else 3
#             logger.info('我的排名:' + str(num))
#             exclude.append(num)
#         
#         r = self(text="没有更多了")
#         __max_tries = 20
#         while 1:
#             if r.wait(timeout=0.1):
#                 if self.is_onscreen(r):
#                     tries = 0
#                     break
#                 else:
#                     if tries > __max_tries:
#                         raise
#                     self.swipe_ext('up', 0.6)
#                     tries += 1
#             else:
#                 if tries > __max_tries:
#                     raise
#                 self.swipe_ext('up', 0.6)
#                 tries += 1
# 
#         r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[1]/android.view.View[1]')
#         while 1:
#             if r.wait(timeout=0.1):
#                 if self.is_onscreen(r):
#                     tries = 0
#                     break
#                 else:
#                     if tries > __max_tries:
#                         raise
#                     self.swipe_ext('down', 0.6)
#                     tries += 1
#             else:
#                 if tries > __max_tries:
#                     raise
#                 self.swipe_ext('down', 0.6)
#                 tries += 1
# 
#         r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]')
#         elem = r.elem
#         for t in elem.getchildren():
#             cs = t.getchildren():
#             c = cs[4].getchildren()
#             if c:
#                 exclude.append(c[0].get('text'))
#            
#         i = start
#         tries = 0
#         while 1:
#             if time.time() - start_time > max_time:
#                 self.screen_off()
#                 return
#             if i in exclude:
#                 i += 1
#                 continue
#             r = self.xpath('//*[@resource-id="__react-content"]/android.view.View[1]/android.view.View[2]/android.view.View[{}]/android.view.View[5]'.format(i))
#             if r.wait(timeout=3):
#                 p = r.screenshot()
#                 p = p.convert('L')
#                 b = l = 0
#                 for c in p.getdata():
#                     l += 1
#                     if c > 240:
#                         b += 1
#                 p = b/l  # 空白率
#                 print(p)
#                 if p < 0.9 and not r.elem.getchildren(): 
#                     # 等待收取时，time_info = r.elem.getchildren() 子节点列表
#                     # 此时包含列表首值 time_info.getchildren().get('text')
#                     # 返回成熟等待时间 11'
#                     r.click()
#                     self.app_wait("com.eg.android.AlipayGphone")
#                     r = self(textContains="收集能量")
#                     if r.wait(timeout=2):
#                         for _ in r:
#                             r.click_exists(timeout=1)
#                             time.sleep(0.3)
#                         exclude.append(i)
#                     else:
#                         r = self(text='\xa0')
#                         r.click_exists()
#                     self.press('back')
# 
#                 if i < end:
#                     i += 1
#                 else:
#                     break
#                 self.swipe_ext("up", 0.05)
#                 tries = 0
#             else:
#                 exclude.append(i)
#                 self.swipe_ext("up", 0.4)
#                 tries += 1
#         
#         if recircle:
#             if end - start - len(exclude) > 5:
#                 for i in range(5):
#                     self.swipe_ext('down', 0.7)
#                     time.sleep(0.1)
#                 recircle += 1
#                 self.alipay_energy(start=start, end=end, exclude=exclude,
#                             mode=mode, recircle=recircle, max_time=max_time,
#                             start_time=start_time, max_tries=10)
#             else:
#                 self.screen_off()
#         else:
#             self.screen_off()
#     
# 
# def alipay_home(self):
#     r = self(text="")
#     # r = self.xpath('//*[@resource-id="com.alipay.mobile.nebula:id/h5_nav_options"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[2]')
#     if r.exists:
#         r.click()
#         self.app_wait("com.eg.android.AlipayGphone")
 
 
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

    if '--friend' in args:
        mode += 4

    kwargs['mode'] = mode
    d.alipay_energy(**kwargs)


load(Device)

if __name__ == "__main__":
    main()

