#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: app.py
# Author: Shechucheng
# Created Time: 2020-07-07 00:17:59

from fire import Fire
from androidbot.wechat import Device

if __name__ == "__main__":
    Fire(Device())
