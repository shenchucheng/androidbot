#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: wechat.py
# Author: Shechucheng
# Created Time: 2020-06-28 23:28:20


import os
import sys
import time

from os.path import join
from .tools import Device, get_bounds, logger
try:
    from .config import storage_path
except:
    storage_path = '/root/Pictures'

def wechat_click_once(self, timeout=20):
    self.wechat_start()
    r = self(resourceId="com.tencent.mm:id/e3x", text="哥哥点进去就可以了")
    # if not r.click_exists(timeout=3):
    #     for i in range(10):
    #         self.swipe_ext('down', 0.5)
    r.click(timeout=3)
    r = self(textContains='聊天记录')
    r.wait()
    info  = {}
    r = list(r)
    r.sort(key=lambda x: x.center()[1])
    r[-1].click()
    r = self(textContains='东东农场')
    r.wait()
    info['东东农场'] = 0 
    for i in r:
        info['东东农场'] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        if self(text="去农场领水滴").wait(timeout=3):
            logger.info('东东农场浇水成功')
        else:
            filename = '东东农场_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            logger.warn('无法确定是否浇水成功，将进行截图处理，文件名：{}'.format(filename))
            self.screenshot(filename)
        back_to_wechat(self)

    self.swipe_ext('up', 0.2)

    r = self(textContains='领养了一只爱宠')
    r.wait()
    info['东东萌宠'] = 0 
    for i in r:
        info['东东萌宠'] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        if self(text="好开心，谢谢帮忙哦！").wait(timeout=5):
            logger.info('东东萌宠助力成功')
        elif self(text="今日助力满员，谢谢你哦~"):
            logger.warn('今日助力满员')
            filename = '东东萌宠_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            self.screenshot(filename)
        else:
            filename = '东东萌宠_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            logger.warn('无法确定是否浇水成功，将进行截图处理，文件名：{}'.format(filename))
            self.screenshot(filename)
        back_to_wechat(self)

    return info


def back_to_wechat(self):
    self.app_start('com.tencent.mm')
    self.app_wait('com.tencent.mm')


def wechat_click_everyday(self, timeout=10):
    self.wechat_start()
    r = self(resourceId="com.tencent.mm:id/e3x", text="每天必点")
    # if not r.click_exists(timeout=3):
    #     for i in range(10):
    #         self.swipe_ext('down', 0.5)
    r.click(timeout=3)
    r = self(textContains='聊天记录')
    r.wait()
    info  = {}
    r = list(r)
    r.sort(key=lambda x: x.center()[1])
    r[-1].click()
    r = self(textContains='东东农场')
    r.wait()
    info['东东农场'] = 0 
    for i in r:
        info['东东农场'] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        if self(text="去农场领水滴").wait(timeout=3):
            logger.info('东东农场浇水成功')
        else:
            filename = '东东农场_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            logger.warn('无法确定是否浇水成功，将进行截图处理，文件名：{}'.format(filename))
            self.screenshot(filename)
        back_to_wechat(self)
    self.swipe_ext('up', 0.2)
    info['财富岛'] = 0
    for i in self(textContains='岛'):
        info['财富岛'] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        if self(textContains='欣然收下').click_exists(timeout=3):
            logger.info('财富岛打工成功')
        elif self(text="每日赚财富").wait(timeout=3):
            logger.info('已经打过工了')
        else:
            filename = '财富岛_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            logger.warn('无法确定是否浇水成功，将进行截图处理，文件名：{}'.format(filename))
            self.screenshot(filename)
        back_to_wechat(self)
    info['多多果园'] = 0
    for i in self(textContains='水果礼'):
        info['多多果园'] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl", text="多多果园").wait(timeout=timeout)
        if self(text="立刻去浇水").click_exists(timeout=15):
            logger.info('多多果园浇水成功')
        elif self(text='选我').click_exists(timeout=10):
            logger.info('多多果园已经浇过水了')
        else:
            filename = '多多果园_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            logger.warn('无法确定是否浇水成功，将进行截图处理，文件名：{}'.format(filename))
            # self.screenshot(filename)
        back_to_wechat(self)
    info['多多牧场'] = 0
    for i in self(textContains='饲料'):
        info['多多牧场'] += 1
        i.click()
        time.sleep(5)
        self(resourceId="com.tencent.mm:id/dl", text="多多牧场").wait(timeout=timeout)
        self(text="送你一个牧场红包").click_exists(timeout=10)
        if self(text="开红包").click_exists(timeout=5):
            logger.info('多多牧场领取饲料成功')
        elif self(text='选我').click_exists(timeout=3):
            logger.info('多多牧场饲料已经领取过了')            
        else:
            filename = '多多牧场_{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'))
            filename = join(storage_path, filename)
            logger.warn('无法确定是否帮助成功，将进行截图处理，文件名：{}'.format(filename))
            self.screenshot(filename)
        back_to_wechat(self)
    return info


def wechat_star(self):
    self.wechat_start()
    self.swipe_ext('down', 0.7)
    r = self(textContains='微信支付集')
    r.click_exists()
    self(text="我的星光").wait(timeout=10)
    for i in range(5):
        self(text="集星光").click()


def wechat_start(self, max_tries=3, timeout=2):
    self.unlock()
    package = "com.tencent.mm"
    self.package_start(package)
    r = self(resourceId="com.tencent.mm:id/cns", text="微信")
    while max_tries:
        if r.click_exists(timeout=timeout):
            return True
        else:
            self.press('back')
            max_tries -= 1
    self.package_start(package, init=True)
    return r.wait(timeout=10)


def load(self):
    self.wechat_start = wechat_start
    self.wechat_click_everyday = wechat_click_everyday
    self.wechat_click_once = wechat_click_once
    self.wechat_star = wechat_star


def main():
    args = sys.argv
    d = Device()
    if 'star' in args:
        d.wechat_star()
        return
    d.wechat_click_everyday()
    d.wechat_click_once()


load(Device)


if __name__ == "__main__":
    main()
     
