#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: androidbot/tools.py
# Author: Shechucheng
# Created Time: 2020-06-24 22:15:48


import time
import logging
import os
# import aircv as ac
import numpy as np

from uiautomator2 import _fix_wifi_addr
from uiautomator2 import Device as Core


logger = logging.getLogger('andriodbot')

# 锁屏密码
_passwd = [(0.25, 0.611),(0.227, 0.841),(0.772, 0.864)]
_src_dir = os.path.abspath(__file__)
_src_dir = os.path.dirname(_src_dir)
_src_dir = os.path.join(_src_dir, 'src')


class Import_lazy:
    def __init__(self, name):
        self.name = name
        self.package = None

    def __getattr__(self, name):
        if not self.package:
            self.package = __import__(self.name)
        self.__dict__[name] = self.package.__getattribute__(name)
        return super().__getattribute__(name)

ac = Import_lazy('aircv')


def platform():
    r = os.system('termux-open')
    if r == 0:
        return 'termux'


def get_bounds(elem):
    return eval(elem.attrib.get('bounds').replace('][', ','))


class Device(Core):
    def __init__(self, serial_or_url=None, **kwargs):
        if kwargs.get('termux'):
            serial_or_url = (_fix_wifi_addr('0.0.0.0'))
        super().__init__(serial_or_url, **kwargs)
    
    def package_start(self, package, init=False):
        self.unlock()
        if init:
            self.session(package)
            self.app_wait(package)
        else:
            self.app_start(package)
            self.app_wait(package)

    def load_images(self, scr_dir=None, **kwargs):
        try:
            self.images
        except:
            self.images = {}
        scr_dir = scr_dir if scr_dir else _src_dir
        for k, v in kwargs.items():
            self.images[k] = np.asarray(
                ac.imread(os.path.join(scr_dir, v))
            )

    def is_screen_on(self):
        return self.info.get('screenOn')

    def is_lock(self):
        packages = {'com.android.systemui', 'android'}
        package = self.info.get('currentPackageName')
        return package in packages 

    def unlock(self, passwd=[]):
        """unlock the screen

        Keyword Arguments:
            passwd {list} -- password swipe points (default: {[]})

        Returns:
            [Bool] -- []
        """
        if not self.is_screen_on():
            self.screen_on()
        # r = self(resourceId="com.android.systemui:id/qs_frame")
        # if r.wait(timeout=3):
        if self.is_lock(): 
            # nolocal _passwd
            passwd = passwd or self.settings.get("passwd") or _passwd
            self.swipe_ext("up", 0.5)
            time.sleep(0.5)
            self.swipe_points(passwd, 0.1)
            return True
        else:
            return 'unlock'
  
    def window_available_info(self):
        try:
            info = self._windows_available_info
        except Exception:
            w, h = self.window_size()
            w0 = 10
            w -= 10
            bar = self(resourceId="com.android.systemui:id/status_bar")
            nav = self(resourceId="com.android.systemui:id/nav_buttons")
            if bar.wait(timeout=1):
                h0 = bar.bounds()[3] + 10
            else:
                h0 = 10

            if nav.wait(timeout=1):
                h = nav.bounds()[1] -10
            else:
                h = h -10
            info = self._windows_available_info = (w0, h0, w, h)
            print('初始化完成')
        return info
        
    def is_onscreen(self, r, info=None, timeout=1):
        if info is None:
           info = self.window_available_info() 
        w0, h0, w, h = info
        if not r.wait(timeout=timeout):
            return False
        try:
            x, y = r.center()
            if y < h0 or y > h or x < w0 or x > w:
                return False
            return True
        except Exception:
            return False
    
    def images_match(self, match, **kwargs):
        scr = np.asarray(self.screenshot())
        return ac.find_all_template(scr, match, **kwargs)

    def images_match_click(self, match, threshold=0.85, **kwargs):
        rs = self.images_match(match, threshold=threshold, **kwargs)
        times = 0
        for i in rs:
            self.click(*i['result'])
            times += 1
        return times

    def back(self, times=1):
        for _ in range(times):
            self.press('back')
            time.sleep(0.3)


class Images:
    images_dict = {}
    srcdir = _src_dir
    def __init__(self, srcdir = '', images_dict = None):
        if srcdir:
            self.srcdir = srcdir
        if images_dict:
            self.images_dict = images_dict
    def __getattr__(self, name):
        Images = super().__self__
        if self.images_dict.get(name) == Images.images_dict.get(name) and \
            self.srcdir == Images.srcdir:
            __self = Images
        else:
            __self = self
        try:
            __path = __self.images_dict[name]
            __path = os.path.join(__self.srcdir, __path)
            setattr(__self, name, np.asanyarray(
                ac.imread(__path)
            ))
        except KeyError:
            logger.exception('Key {} has not existed in image_dict'.format(name))
        except RuntimeError:
            logger.exception('Please check the file path or the srcdir', exc_info=True)
        try:
            return super().__getattr__(name)
        except AttributeError:
            return super().__getattribute__(name)


class App(object):
    def __init__(self, package, device: Device = None,):
        self.device = device or Device()
        self.__package = package
    
    @property
    def name(self):
        return self.__package

    def start(self, init=False):
        self.device.unlock()
        if init:
            self.device.session(self.name)
            self.device.app_wait(self.name)
        else:
            self.device.app_start(self.name)
            self.device.app_wait(self.name)
            if not self.check_start():
                self.start(init=True)
    
    def check_start(self):
        logger.warn('Method for checking status when app {} start is not set'.format(
            self.name
        ))
        return True


class MaxtriesError(Exception):
    def __init__(self, max_tries):
        self.max_tries = max_tries
        self.message = 'Max retries ({} times)'.format(max_tries)


def main():
    d = Device()
    if d.is_screen_on():
        d.screen_off()
    r = d.unlock()
    # logger.info(str(r))
    print(r)


if __name__ == "__main__":
    main()
     
