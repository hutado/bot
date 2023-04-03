#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher


# Настройки бота
DP = Dispatcher(Bot(token=os.getenv('BOT_TOKEN')))
