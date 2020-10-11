#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import os
import sys
import time

from threading import Thread
from collections.abc import Iterable

from .tools import Images, App, Device, get_bounds, MaxtriesError, logger


__d = {
    'hand'       : 'hand.jpg',
    'heart'      : 'heart.jpg',
    'help'       : 'help.jpg',
    'help1'      : 'help1.jpg',
    'gain'       : 'gain.jpg',
    'nomore'     : 'nomore.jpg',
    'nextfriend' : 'nextfriend.jpg'
}

images = Images(images_dict=__d)


class AppAlipay(App):
    def __init__(self, device: Device=None):
        super().__init__('com.eg.android.AlipayGphone', device)

    def check_start(self, max_tries=3):
        r = self.device(resourceId='com.alipay.android.phone.openplatform:id/tab_description')
        while max_tries > 0:
            if r.wait(timeout=1):
                r.click()
                return True
            else:
                self.device.back()
                max_tries -= 1
    
    def sign(self, timeout=5, retry=1):
        self.start()
        if not self.__sign(timeout=timeout) and retry:
            self.sign(timeout=timeout, retry=retry-1)
        else:
            logger.warning('支付宝签到失败')
            
    def __sign(self, timeout=5):
        r = self.device(
            resourceId="com.alipay.android.phone.wealth.home:id/tab_description",
            text='我的'
        )  # 支付宝个人中心
        if not r.click_exists(timeout=timeout):
            return
        time.sleep(0.5)
        if not self.device.xpath('//*[@resource-id="com.alipay.android.phone.wealth.home:id'\
            '/asset_home_list"]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/'\
            'android.view.ViewGroup[1]').click_exists(timeout=timeout):
            return
        if not self.device(text="领积分").click_exists(timeout=timeout):
            return
        __retry = 0
        r = self.device(text="可用积分")
        r.wait(timeout=timeout)
        times = 0
        while 1:
            start = time.time()
            times += 1
            if self.device(text="点击领取").click_exists(timeout=timeout):
                logger.debug('积分收取成功')
            elif time.time() - start >= timeout:
                break
            if times > 40:
                break
            elif times > 10:
                try:
                    __last = ''
                    __last = self.device(text="可用积分").from_parent().child()[1].get_text()
                    if last == __last:
                        break
                except Exception:
                    last = __last
        if self.device(textContains='家庭积分').click_exists(timeout=timeout):
            self.device(text="家庭积分").wait(timeout=timeout)
            while 1:
                start = time.time()
                if self.device(text="积分").click_exists(timeout=timeout):
                    continue
                elif time.time() - start >= timeout:
                    break
            self.device.back()
        self.device.back(2)
        logger.info('支付宝签到成功')
        return True

    def energy(self, mode: int = 7, quality=None, **kwargs):
        self.energy_page()
        if mode in [1, 3, 5, 7]:
            self._energy_self(**kwargs)

        if mode in [2, 3, 6, 7]:
            self._energy_love(quality=quality, **kwargs)

        if mode in [4, 5, 6, 7]:
            self._energy_friends(**kwargs)

        self.device.back(2)

    def energy_self(self, **kwargs):
        self.energy_page()
        self._energy_self(**kwargs)

    def energy_love(self, **kwargs):
        self.energy_page()
        self._energy_love(**kwargs)

    def energy_friends(self, **kwargs):
        self.energy_page()
        self._energy_friends(**kwargs)

    def energy_page(self, timeout=10, retry=0):
        self.start()
        r = self.device(resourceId="com.alipay.android.phone.openplatform:id/app_text", text="蚂蚁森林")
        r.click_exists(timeout=timeout)
        if self.device(text="背包").wait(timeout=5):
            logger.debug('进入蚂蚁森林页面')
        else:
            logger.warn('无法定位蚂蚁森林页面识别元素')
            if not retry:
                self.energy_page(timeout=timeout, retry=1)

    
    def _energy_self(self, patrol = False, duration: int = 180, **kwargs):
        start = time.time()
        stop = False
        while time.time() - start <= duration:
            r = self.device(textContains='收集能量')
            if r.wait(timeout=10):
                logger.info(r.get_text())
                r.click_exists()
                stop = True
            elif not patrol:
                break
            elif patrol == 2 and stop:
                break
            self.device.click(0,0)  # 保持常亮 

    def _energy_love(self, timeout=5, quality=None, **kwargs):
        if kwargs.get('quality_max'):
            quality = 2
        elif kwargs.get('quality_min'):
            quality = 1
        if not self.device(text='合种').click_exists(timeout=timeout):
            return
        if not self.device(text="今日排行").wait(timeout=timeout):
            return
        r = self.device.xpath('//*[@resource-id="J-dom"]/android.view.View[1]/android.view.View[6]/android.view.View[1]/android.view.View[1]')
        if r.click_exists(timeout=5):
            r = self.device(text='浇水')
            if r.wait(timeout=3):
                r.click()
                logger.debug('合种浇水成功')
            else:
                if self.device(text='在该合种浇水已达上限，明天继续哟').wait(timeout=1):
                    logger.debug('今日已经浇过水了')
                self.device(text='知道了').click_exists()
        
        try:
            quality = [None, '10克',  '66克'][quality]
        except Exception:
            pass

        if quality is None:
            self.device.back(1)
            return

        for i in [2, 1]:
            r = self.device.xpath('//android.widget.ListView/android.view.View[{}]'.format(i))
            if r.wait(timeout=timeout):
                r.click()
            r = self.device(text='浇水')
            if r.wait(timeout=4):
                break
            else:
                self.device.press('back')
        for _ in range(3):
            _ = 0
            for i in ['浇水', quality, '浇水送祝福']:
                if self.device(text=i).click_exists(timeout=3):
                    time.sleep(0.5)
                    _ += 1
                else:
                    break
            if _ == 3:
                logger.debug('帮忙浇水{}'.format(quality))
            else:
                logger.warning('帮忙浇水失败')
        self.device.back(2)

    def _energy_friends(self, timeout: int = 3, **kwargs):
        r = self.device(textContains='收集能量')
        while self.nextfriend:
            p0 = (0, 0)
            while r.wait(timeout=timeout):
                try:
                    p1 = r.center()
                except:
                    continue
                if p0 == p1:
                    break
                p0 = p1
                if r.click_exists():
                    time.sleep(0.5)
        if self.device(textContains="startapp?appId").wait(timeout=5):
            self.device.back()
            return
        if self.device(resourceId="com.alipay.mobile.nebula:id/h5_tv_title", text="蚂蚁森林").wait(timeout=1):
            return

    @property
    def nextfriend(self, threshold=0.8, **kwargs):
        r = self.device.images_match_click(images.nextfriend, threshold=threshold, **kwargs)
        if r > 1:
            logger.warning('支付宝蚂蚁森林逛一逛匹配多个结果')
        return bool(r)
    
    def getnextfriendposition(self):
        if not hasattr(self, '__position'):
            self.__position = None
        if not self.__position:
            Thread(self.position)
    
    def position(self):
        r = self.device.images_match(images.nextfriend, threshold=0.8)
        for _ in r:
            self.__position = _['result']


if __name__ == '__main__':
    from fire import Fire
    Fire(AppAlipay())


# 识别图片字典



# def noexists_raise(timeout=1, max_tries=5):
#     while 1:
#         if r.wait(timeout=timeout):
#             tries = 0
#             return True
#         else:
#             if tries >= max_tries:
#                 raise 
#             tries += 1

      
def get_next_time(self):
    pass


def energy_friend_locate(self):
    pass


# 获取好友列表
def friends_list(self):
    """获取蚂蚁森林好友列表

    Returns:
        [type] -- [description]
    """
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
    """处理蚂蚁森林好友列表信息

    Arguments:
        friend {[type]} -- [description]
        i {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
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
    # r = self(text='总排行榜')
    r = self(resourceId="com.alipay.mobile.nebula:id/h5_tv_title", text="蚂蚁森林")
    r.wait(timeout=timeout)
    rs = self.images_match(self.images['hand'], threshold=threshold, **kwargs)
    if not rs:
        if self.images_match(self.images['nomore'], threshold=threshold, **kwargs):
            return 'STOP'
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
            try:
                if r.wait(timeout=1):
                    p = r.center()
                    if p == p0:
                        break
                    p0 = p
                    r.click()
                    time.sleep(0.3)
                else:
                    break
            except:
                break
    else:
        # if self(text='总排行榜').wait(timeout=1):
        if self(textContains="startapp?appId").wait(timeout=5):
            self.press('back')
            return
        if self(resourceId="com.alipay.mobile.nebula:id/h5_tv_title", text="蚂蚁森林").wait(timeout=1):
            return
        
    for p in ['help', 'help1']:
        self.images_match_click(self.images[p], threshold=threshold)
    if self.images_match_click(self.images['nextfriend'], threshold=threshold):
        energy_gain(self, timeout=timeout, threshold=threshold, **kwargs)
    else:
        self.press('back')



def is_friend_list_page(self):
    """判断页面位置

    Returns:
        bool -- 当前页面是否位于好友列表
    """
    return True


def energy_next_page(self, reverse=False, rate=0.5):
    """好友列表翻页

    Keyword Arguments:
        reverse {bool} -- 翻页方向 (default: {False})
        rate {float} -- 翻页比例 (default: {0.5})
    """
    if reverse:
        self.swipe_ext('down', rate)
    else:
        self.swipe_ext('up', rate)
    

def energy_friends_gain(self, plus=False, max_tries=30):
    r = self(text='没有更多了')
    while max_tries and not self.is_onscreen(r):
        if energy_page(self, plus=plus) == 'STOP':
            break
        energy_next_page(self)
        max_tries -= 1


def energy_friends(self, timeout=1, max_tries=5, **kwargs):
    tries = 0
    start_time = kwargs.get('start_time') or time.time()
    for i in range(5):
        if self.images_match_click(self.images['nextfriend'], threshold=0.85):
            energy_gain(self)
            return
        time.sleep(1)
    r = self(text='查看更多好友')
    # noexists_raise()
    while not self.is_onscreen(r):
        if tries >= max_tries:
            raise MaxtriesError(max_tries)
        tries += 1
        self.swipe_ext('up', 0.6)
    r.click()
    time.sleep(0.5)
    # self(text='总排行榜').click()
    energy_friends_gain(self, plus=kwargs.get('plus'))
    if kwargs.get('recircle'):
        if kwargs.get('fix'):
            max_time = kwargs.get('max_time') or 1200
            num = 0
            while time.time() - start_time < max_time:
                num = energy_friends_walk(self, num=num)
                if not num:
                    break
        else:
            for i in range(kwargs.get('circle_times') or 5):
                for i in range(8):
                    energy_next_page(self, True, 0.7)
                    time.sleep(0.2)
                energy_friends_gain(self)



def energy_friends_walk(self, num):
    """移动到指定排名好友位置

    Arguments:
        num {init, list} -- [排名]

    Returns:
        [init, list] -- [下次排名]
    """
    if num == 0:
        t, num = get_next_time(self)
        time.sleep(t)
        return num
    elif Iterable(num):
        for i in num:
            energy_friends_walk(self, num=i)
    elif type(num) == int:
        energy_friends_to(self, num)


def energy_friends_to(self, num):
    """到指定排名好友摘取能量

    Arguments:
        num {init, Iterable} -- [指定排名]
    """
    # 页面
    # 指定位置
    # 摘取能量
    pass
    

def energy_self_love(self, timeout=3):
    p = self.images.get('energyball')
    if p is None:
        self.load_images(energyball='energyball.jpg')
        p = self.images['energyball']
    return self.images_match_click(p, threshold=0.8)


def energy_self(self, max_tries=10):
    tries = 1
    times = 0
    while 1:
        energy_self_love(self)
        times += 1
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
    while times < 3:
        energy_self_love(self)
        times += 1


def energy_love(self, timeout=10, **kwargs):
    r = self(text='合种')
    r.click(timeout=timeout)
    r = self.xpath('//*[@resource-id="J-dom"]/android.view.View[1]/android.view.View[6]/android.view.View[1]/android.view.View[1]')
    r.click(timeout=timeout)
    if self(text='浇水').click_exists(timeout=4):
        pass
    elif self(text='在该合种浇水已达上限，明天继续哟').wait(timeout=3):
        self(text='知道了').click()
    else:
        logger.warn('蚂蚁森林合种浇水错误')
        return False

    for i in range(1, 3):
        r = self.xpath('//android.widget.ListView/android.view.View[{}]'.format(i))
        r.click()
        r = self(text='浇水')
        if r.wait(timeout=4):
            break
        else:
            self.press('back')
    g = kwargs.get('quality') or '10克'
    for _ in range(3):
        for i in ['浇水', g, '浇水送祝福']:
            self(text=i).click_exists(timeout=3)
            time.sleep(1)
        print('{}'.format(g))
    self.press('back')
    self.press('back')


def alipay_sign(self, init=True, timeout=3, **kwargs):
    """支付宝签到

    Keyword Arguments:
        init {bool} -- 重启 (default: {True})
        timeout {int} -- 超时时间 (default: {3})
    """
    self.alipay_start()
    path = [
        self(resourceId="com.alipay.android.phone.wealth.home:id/tab_description"),
        self(resourceId="com.alipay.mobile.antui:id/item_left_text", text="支付宝会员"),
    ]
    for r in path:
        if r.wait(timeout=timeout):
            r.click()
        else:
            return 0
    t = 1
    if not self(text="领积分").click_exists(timeout=timeout):
        self.press('back')
        return 0
    self.device(text="家庭积分").wait(timeout=timeout)
    while self(text="点击领取").click_exists(timeout=timeout):
        continue
    time.sleep(3)
    path = [
        self.xpath('//*[@resource-id="app"]/android.view.View[2]/android.view.View[2]/android.view.View[1]'),
        self.xpath('//*[@text="领取每日签到积分"]/android.view.View[1]')
    ]
    t = 2
    for r in path:
        if r.wait(timeout=timeout):
            r.click()
        else:
            t = 1
            break
    for _ in range(t+1):
        self.press('back')
    return t


def alipay_energy_start(self):
    self.alipay_start()
    r = self(resourceId="com.alipay.android.phone.openplatform:id/app_text", text="蚂蚁森林")
    if not r.wait(timeout=3):
        self.alipay_start(init=1)
    r.click()


def alipay_energy(self, mode=0, plus=0, **kwargs):
    start_time = time.time()
    alipay_energy_start(self)

    if mode in [1, 3, 5, 7]:
        energy_self(self)
        if mode == 1:
            self.press('back')
            self.press('home')
            self.screen_off()
            return

    if mode in [2, 3, 6, 7]:
        energy_love(self, **kwargs)
        if mode == 2:
            self.press('back')
            self.press('home')
            self.screen_off()
            return
        
    if mode == 3:
        return

    energy_friends(self, plus=plus, **kwargs)

    self.press('back')
    self.press('back')
    self.press('home')
    self.screen_off()
    duration = time.time() - start_time
    return duration


def alipay_fruit(self, timeout=5):
    self.alipay_start()
    self(resourceId="com.alipay.mobile.socialwidget:id/social_tab_text").click(timeout=timeout)
    self(resourceId="com.alipay.mobile.socialwidget:id/item_memo", text="[小程序]饿了么果园").click(timeout=timeout)
    self(resourceId="com.alipay.mobile.chatapp:id/biz_title", text="快帮我助力免费领3斤水果").click(timeout=timeout)
    self(text="帮TA助力").click(timeout=10)


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
    self.alipay_start  = alipay_start
    self.alipay_energy = alipay_energy
    self.alipay_sign   = alipay_sign
    self.alipay_fruit  = alipay_fruit
    self.images = {}
    self.load_images(self, **images_dict)


def main():
    args = sys.argv
    d = Device()
    kwargs = {}
    mode = 0
    if len(args) > 1 and args[1] == 'sign':
        d.alipay_sign()
        return
    if len(args) > 1 and args[1] == 'fruit':
        d.alipay_fruit()
        return
    if '--plus' in args:
        kwargs['plus'] = 1

    if '--self' in args:
        mode += 1

    if '--love' in args:
        if '--quality-max' in args:
            kwargs['quality'] = '66克'
        mode += 2

    if '--friends' in args:
        mode += 4
    if '--recircle' in args:
        kwargs['recircle'] = True
    kwargs['mode'] = mode
    d.alipay_energy(**kwargs)


# load(Device)

# if __name__ == '__main__':
#     main()

