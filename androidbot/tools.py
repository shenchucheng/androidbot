#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/tools.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:48


import uiautomator2


__passwd = [(0.25, 0.611),(0.227, 0.841),(0.772, 0.864)]


def is_screen_on(self):
    return self.info.get('screenOn')


def unlock(self, passwd=[]):
    if not is_screen_on(self):
        self.screen_on()
    r = self(resourceId="com.android.systemui:id/qs_frame")
    if r.exists(timeout=3):
        passwd = passwd or self.settings.get("passwd") or __passwd
        self.swipe_ext("up", 0.3)
        self.swipe_points(passwd, 0.1)


def main():
    d = uiautomator2.connect()
    unlock(d)


if __name__ == "__main__":
    main()
     
