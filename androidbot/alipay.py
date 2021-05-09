#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/alipay.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:20


import os
import sys
import time

from threading import Thread
from os.path import join
from collections.abc import Iterable

from .tools import Images, App, Device, get_bounds, MaxtriesError, logger
try:
    from .config import storage_path
except:
    storage_path = "."

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

    def msg(self, timeout=5, retry=1):
        self.start()
        if not self.__msg(timeout=timeout) and retry:
            return self.msg(timeout=timeout, retry=retry-1)

    def __msg(self, timeout):
        if not self.device(
            resourceId="com.alipay.mobile.socialwidget:id/social_tab_text"
        ).click_exists(timeout=3):
            return 
        if not self.device(
            resourceId="com.alipay.mobile.socialwidget:id/item_name", text="颖灵"
        ).click_exists(timeout=3):
            return

        src = self.device(textContains="肥料到手")
        src.wait(timeout=timeout)
        for i in src:
            i.click(timeout=timeout)
            self.device(text="为Ta助力").wait(timeout=timeout)
            self.device(text="为Ta助力").click(timeout=timeout)
            self.device(text="去种果树").wait(timeout=timeout)
            filename = "芭芭农场_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
            filename = join(storage_path, filename)
            self.device.screenshot(filename)
            self.device(text="").click_exists(timeout=timeout)
            self.device(textContains="肥料到手").wait(timeout=timeout)

        src = self.device(
            resourceId="com.alipay.mobile.chatapp:id/biz_title", text="送你1箱免费水果"
        )
        src.wait(timeout=timeout)
        for i in src:
            i.click(timeout=timeout)
            self.device(text="帮TA助力").wait(timeout=timeout)
            self.device(text="帮TA助力").click_exists(timeout=timeout)
            filename = "饿了吗果园_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
            filename = join(storage_path, filename)
            self.device.screenshot(filename)
            self.device(text="").click_exists(timeout=timeout)

        return True
        
    def sign(self, timeout=5, retry=1):
        self.start()
        if not self.__sign(timeout=timeout) and retry>0:
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
            if kwargs.get('plus'):
                try:
                    for ui in self.device(resourceId="J_barrier_free").child():
                        if ui.get_text() == '\xa0':
                            ui.click_exists()
                except Exception:
                    continue
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
    # AppAlipay().msg()
