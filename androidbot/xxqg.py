#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/xxqg.py
# Author: Shechucheng
# Created Time: 2021-06-12 15:13:43


import time

from androidbot.tools import Device, logger, App


class XXQGApp(App):
    _package = "cn.xuexi.android"

    def check_start(self, max_tries=3):
        d = self.device
        r = d(resourceId="cn.xuexi.android:id/home_bottom_tab_icon_large")
        while max_tries > 0:
            if r.wait(timeout=1):
                r.click()
                return True
            else:
                d.back()
                max_tries -= 1

def main():
    app = XXQGApp()
    app.start()
    app.check_start()


if __name__ == "__main__":
    main()