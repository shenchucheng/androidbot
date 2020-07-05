#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: wechat.py
# Author: Shechucheng
# Created Time: 2020-06-28 23:28:20


import os
import sys
import time

from .tools import Device, get_bounds, logger


def wechat_start(self):
    self.unlock()
    self.app_start("com.tencent.mm")
    self.app_wait("com.tencent.mm")
    r = self(resourceId="com.tencent.mm:id/cns", text="通讯录")
    tries = 1
    while 1:
        if r.wait(timeout=2):
            self(resourceId="com.tencent.mm:id/cns", text="微信").click()
            break
        else:
            self.press('back')
            tries += 1
        if tries > 10:
            raise


def load(self):
    self.wechat_start = wechat_start


def main():
    d = Device()
    d.wechat_start()


load(Device)
if __name__ == "__main__":
    main()
     
