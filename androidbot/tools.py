#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/tools.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:48


import time
import logging
import os


from uiautomator2 import Device


logger = logging.getLogger('andriodbot')

# 锁屏密码
__passwd = [(0.25, 0.611),(0.227, 0.841),(0.772, 0.864)]


def is_screen_on(self):
    return self.info.get('screenOn')


def is_lock(self):
    return self.info.get('currentPackageName') ==  'com.android.systemui'


def unlock(self, passwd=[]):
    """
    屏幕解锁
    """
    if not is_screen_on(self):
        self.screen_on()
    # r = self(resourceId="com.android.systemui:id/qs_frame")
    # if r.wait(timeout=3):
    if self.is_lock: 
        passwd = passwd or self.settings.get("passwd") or __passwd
        self.swipe_ext("up", 0.5)
        time.sleep(0.5)
        self.swipe_points(passwd, 0.1)


def platform():
    r = os.system('termux-open')
    if r == 0:
        return 'termux'


def load(self):
    self.is_screen_on = is_screen_on
    self.is_lock      = is_lock
    self.unlock       = unlock


def main():
    if platform == 'termux':
        d = Device('0.0.0.0')
    else:
        d = Device()

    if d.is_screen_on():
        d.screen_off()
    r = d.unlock()
    # logger.info(str(r))
    print(r)


load(Device)

if __name__ == "__main__":
    main()
     
