#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# File Name: wechat.py
# Author: Shechucheng
# Created Time: 2021-05-14 23:28:20

from fire import Fire
from androidbot.wechat import Device


if __name__ == "__main__":
    Fire(Device())
