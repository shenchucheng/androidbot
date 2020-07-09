#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/browser.py
# Author: Shechucheng
# Created Time: 2020-07-08 08:08:20


import time


from .tools import Device, logger


def browser_start(self, init=False, timeout=5):
    package='com.android.browser'
    self.package_start(package)
    r = self(resourceId="com.android.browser:id/action_info")
    if r.click_exists(timeout=timeout):
        return True
    else:
        return self.package_start(package, init=1)


def browser_persion(self, timeout=5):
    r = self(resourceId="com.android.browser:id/action_person")
    return r.click(timeout=timeout)


def browser_sign(self, timeout=5):
    self.browser_start()
    browser_persion(self)
    r = self(text="每日任务").wait(timeout=timeout)
    if self(text="签到").click_exists(timeout=timeout):
        if self(textContains="签到成功").wait(timeout=10):
            self.press('back')
    if not r:
        self(text='已签到').click()
    r1 = browser_sign_video(self)
    r2 = browser_sign_article(self)
    self(textContains='金币待领取').click_exists(timeout=timeout)
    time.sleep(1)
    r3 = browser_sign_search(self)
    if r3:
        self(textContains='金币待领取').click_exists(timeout=timeout)
    r4 = browser_sign_advert(self)
    r = self(text="领取奖励")
    while r.click_exists(timeout=timeout):
        self(textContains='知道').click_exists(timeout=timeout)
    return r1, r2, r3, r4


def browser_sign_advert(self):
    r = self(text='去完成')
    if len(r) >= 2:
        y = self(textContains='搜索想问的问题').center()[1]
        r = list(r)
        r.sort(key=lambda x: abs(y-r.center()[1]))
        r = r[0]
    if r.click_exists():
        ad = self(resourceId="com.android.browser:id/tt_video_ad_close")
        for i in range(4):
            time.sleep(35)
            if ad.click_exists(timeout=timeout):
                break
            self.press('back')
            r.click()
    self.press('back')


def browser_sign_search(self):
    r = self(text='去完成')
    if len(r) >= 2:
        y = self(textContains='搜索想问的问题').center()[1]
        r = list(r)
        r.sort(key=lambda x: abs(y-r.center()[1]))
        r = r[0]
    if r.click_exists():
        r = self.xpath('//*[@resource-id="com.android.browser:id/vo_hot_search_gv"]/android.widget.RelativeLayout[1]')
        r.click()
        time.sleep(1)
        self.press('back')
        time.sleep(1)
        self(resourceId="com.android.browser:id/search").click()
        r = self.xpath('//*[@resource-id="com.android.browser:id/vo_hot_search_gv"]/android.widget.RelativeLayout[1]')
        r.click()
        time.sleep(1)
        self.press('back')
        return browser_persion(self)


def browser_sign_article(self, timeout=5, check=False):
    r = self(textContains='浏览资讯文章')
    if not r.wait(timeout=timeout):
        return self(text="每日任务").wait(timeout=timeout)
    text = r.get_text()
    rest = get_rest(text)
    if rest == 0:
        return True
    r.click()
    r = self.xpath('//*[@resource-id="com.android.browser:id/common_recycler_view"]/android.widget.LinearLayout')
    r.click(timeout=timeout)
    for _ in range(round(20*rest+1)):
        time.sleep(15) 
        self.swipe_ext('up', 0.5)
    self.press('back')
    return browser_persion(self)


def get_rest(text):
    text = text.split('/')
    a, b = eval(text[0][-1]), eval(text[1][0])
    return 1 - a/b


def browser_sign_video(self, timeout=5, check=False):
    r = self(textContains='观看小视频')
    if not r.wait(timeout=timeout):
        return self(text="每日任务").wait(timeout=timeout)
    text = r.get_text()
    rest = get_rest(text)
    if rest == 0:
        return True
    r.click()
    r = self.xpath('//*[@resource-id="com.android.browser:id/common_recycler_view"]/android.widget.RelativeLayout[1]')
    r.click(timeout=timeout)
    for _ in range(round(20*rest+1)):
        time.sleep(15) 
        self.swipe_ext('up', 0.5)
    self.press('back')
    return browser_persion(self)


def load(self):
    self.browser_start = browser_start
    self.browser_sign  = browser_sign


load(Device)


def main():
    d = Device()
    d.browser_sign()

if __name__ == "__main__":
    main()