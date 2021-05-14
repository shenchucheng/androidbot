#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: wechat.py
# Author: Shechucheng
# Created Time: 2020-06-28 23:28:20


import os
import sys
import time

from os.path import join

from numpy import imag
from .tools import Device, get_bounds, logger, Images
try:
    from .config import storage_path
except:
    storage_path = "."

__d = {
    'wechat_accept_work'       : 'wechat_accept_work.jpg',
}

images = Images(images_dict=__d)


def wechat_click_once(self, timeout=20):
    self.wechat_start()
    r = self(resourceId="com.tencent.mm:id/e3x", text="哥哥点进去就可以了")
    # if not r.click_exists(timeout=3):
    #     for i in range(10):
    #         self.swipe_ext("down", 0.5)
    r.click(timeout=3)
    r = self(textContains="聊天记录")
    r.wait()
    info  = {}
    r = list(r)
    r.sort(key=lambda x: x.center()[1])
    r[-1].click()
    r = self(textContains="东东农场")
    r.wait()
    info["东东农场"] = 0 
    for i in r:
        info["东东农场"] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        if self(text="去农场领水滴").wait(timeout=3):
            logger.info("东东农场浇水成功")
        else:
            filename = "东东农场_{}.jpg".format(time.strftime("%Y%m%d%H%M%S"))
            filename = join(storage_path, filename)
            logger.warn("无法确定是否浇水成功，将进行截图处理，文件名：{}".format(filename))
            self.screenshot(filename)
        back_to_wechat(self)

    self.swipe_ext("up", 0.2)

    r = self(textContains="领养了一只爱宠")
    r.wait()
    info["东东萌宠"] = 0 
    for i in r:
        info["东东萌宠"] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        if self(text="好开心，谢谢帮忙哦！").wait(timeout=5):
            logger.info("东东萌宠助力成功")
        elif self(text="今日助力满员，谢谢你哦~"):
            logger.warn("今日助力满员")
            filename = "东东萌宠_{}.jpg".format(time.strftime("%Y%m%d%H%M%S"))
            filename = join(storage_path, filename)
            self.screenshot(filename)
        else:
            filename = "东东萌宠_{}.jpg".format(time.strftime("%Y%m%d%H%M%S"))
            filename = join(storage_path, filename)
            logger.warn("无法确定是否浇水成功，将进行截图处理，文件名：{}".format(filename))
            self.screenshot(filename)
        back_to_wechat(self)

    return info


def back_to_wechat(self):
    self.app_start("com.tencent.mm")
    self.app_wait("com.tencent.mm")


def work_erveryday(self: Device, times: int = 0):
    self.wechat_start()
    r = self(resourceId="com.tencent.mm:id/fzg", text="打工工专用用")
    r.click(timeout=3)
    r = self(textContains="聊天记录")
    r.wait()
    r = list(r)
    r.sort(key=lambda x: x.center()[1])
    r[-1].click()
    r = self(textContains="【1.09上新】")
    r.wait()
    r = list(r)[times]
    r.click()
    for i in range(3):
        time.sleep(3)
        if self.images_match_click(images.wechat_accept_work):
            break
    self.click(0.5, 0.689)
    time.sleep(1)
    filename = "京喜工厂_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
    filename = join(storage_path, filename)
    self.screenshot(filename)
    back_to_wechat(self)

def wechat_click_everyday(self, timeout=10):
    self.wechat_start()
    r = self(resourceId="com.tencent.mm:id/fzg", text="每天必点")
    # if not r.click_exists(timeout=3):
    #     for i in range(10):
    #         self.swipe_ext("down", 0.5)
    r.click(timeout=3)
    r = self(textContains="聊天记录")
    r.wait()
    info  = {}
    r = list(r)
    r.sort(key=lambda x: x.center()[1])
    r[-1].click()
    r = self(textContains="东东农场")
    r.wait()

    info["东东农场"] = 0 
    for i in r:
        info["东东农场"] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        time.sleep(3)
        filename = "东东农场_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
        filename = join(storage_path, filename)
        self.screenshot(filename)
        back_to_wechat(self)

    r = self(textContains="超大年终奖金")
    r.wait(timeout=timeout)
    info["财富岛"] = 0
    for i in r:
        info["财富岛"] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        time.sleep(3)
        filename = "财富岛_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
        filename = join(storage_path, filename)
        self.screenshot(filename)
        back_to_wechat(self)
    
    for i in range(3):
        self.swipe_ext('up')
        time.sleep(0.5)

    r = self(textContains="领养了一只爱宠")
    r.wait(timeout=timeout)
    info["多多牧场"] = 0
    for i in r:
        info["多多牧场"] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        time.sleep(3)
        self.click(0.48, 0.669)
        time.sleep(1)
        self.click(0.662, 0.912)
        time.sleep(1)
        filename = "多多牧场_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
        filename = join(storage_path, filename)
        self.screenshot(filename)
        back_to_wechat(self)

    r = self(textContains="帮我点一下")
    r.wait(timeout=timeout)
    info["苏宁农场"] = 0
    for i in r:
        info["苏宁农场"] += 1
        i.click()
        self(resourceId="com.tencent.mm:id/dl").wait(timeout=timeout)
        time.sleep(3)
        self.click(0.496, 0.638)
        time.sleep(3)
        filename = "苏宁农场_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
        filename = join(storage_path, filename)
        self.screenshot(filename)
        back_to_wechat(self)
    
    self.back()

    info["京喜农场"] = 0
    r = self(textContains="你也有机会")
    r.wait(timeout=timeout)
    for i in r:
        i.click()
        info["京喜农场"] += 1
        time.sleep(3)
        filename = "京喜农场_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
        filename = join(storage_path, filename)
        self.screenshot(filename)
        back_to_wechat(self)

    time.sleep(2)
    for i in range(2):
        self.swipe_ext('down', 0.8)
        time.sleep(1)

    r = self(textContains="给春日出游加点料")
    r.wait(timeout=timeout)
    for i in r:
        i.click()
        info["京喜农场"] += 1
        time.sleep(3)
        filename = "京喜农场_{}.jpg".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
        filename = join(storage_path, filename)
        self.screenshot(filename)
        back_to_wechat(self)

    return info


def wechat_star(self):
    self.wechat_start()
    self.swipe_ext("down", 0.7)
    r = self(textContains="微信支付集")
    r.click_exists()
    self(text="我的星光").wait(timeout=10)
    for i in range(5):
        self(text="集星光").click()


def wechat_start(self, max_tries=3, timeout=2):
    self.unlock()
    package = "com.tencent.mm"
    self.package_start(package)
    r = self(resourceId="com.tencent.mm:id/dub", text="微信")
    while max_tries:
        if r.click_exists(timeout=timeout):
            return True
        else:
            self.press("back")
            max_tries -= 1
    self.package_start(package, init=True)
    return r.wait(timeout=10)


def load(self):
    self.wechat_start = wechat_start
    self.wechat_click_everyday = wechat_click_everyday
    self.wechat_click_once = wechat_click_once
    self.wechat_star = wechat_star
    self.work_erveryday = work_erveryday


def main():
    args = sys.argv
    d = Device()
    if "star" in args:
        d.wechat_star()
        return
    d.wechat_click_everyday()
    # d.wechat_click_once()


load(Device)


if __name__ == "__main__":
    main()
     
