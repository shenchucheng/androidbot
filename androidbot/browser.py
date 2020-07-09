#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/browser.py
# Author: Shechucheng
# Created Time: 2020-07-08 08:08:20


import time


from .tools import Device, logger


def browser_start(self, init=False, timeout=5):
    package='com.android.browser'
    self.unlock()
    if init:
        self.session(package)
        self.app_wait(package)
        return True
    else:
        self.app_start(package)
        self.app_wait(package)
        r = self(resourceId="com.android.browser:id/action_info")
        if r.click_exists(timeout=timeout):
            return True
        else:
            return self.browser_start(init=1, timeout=timeout)


def browser_persion(self, timeout=5):
    self.browser_start()
    r = self(resourceId="com.android.browser:id/action_person")
    return r.click_exists(timeout=timeout)


def browser_sign(self, timeout=5):
    self.browser_start()
    browser_persion(self)
    r = self(text="每日任务")
    r1 = browser_sign_video(self)
    if not r1:
        return False
    r2 = browser_sign_article(self)
    if not r2:
        return False
    self(text="去完成").click_exists()
    r = self(text="领取奖励")
    while r.click_exists(timeout=timeout):
        continue


def browser_sign_advert(self):
    pass


def browser_sign_article(self, timeout=5, check=False):
    r = self(textContains='浏览资讯文章')
    text = r.get_text()[8:11]
    rest = 1 - eval(text)
    if rest == 0:
        return True
    r.click()
    r = self.xpath('//*[@resource-id="com.android.browser:id/common_recycler_view"]/android.widget.LinearLayout[1]')
    r.click(timeout=timeout)
    for _ in range(round(20*rest)):
        time.sleep(15) 
        self.swipe_ext('up', 0.5)
    self.press('back')
    return browser_sign(self)


def browser_sign_video(self, timeout=5, check=False):
    r = self(textContains='观看小视频')
    text = r.get_text()[7:10]
    rest = 1 - eval(text)
    if rest == 0:
        return True
    r.click()
    r = self.xpath('//*[@resource-id="com.android.browser:id/common_recycler_view"]/android.widget.RelativeLayout[1]')
    r.click(timeout=timeout)
    for _ in range(round(20*rest)):
        time.sleep(15) 
        self.swipe_ext('up', 0.5)
    self.press('back')
    return browser_sign(self)


def load(self):
    self.browser_start = browser_start
    self.browser_sign  = browser_sign


load(Device)


def main():
    d = Device()
    d.browser_sign()

if __name__ == "__main__":
    main()