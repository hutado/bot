#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import datetime

import feedparser

from aiogram import types
from aiogram.utils import executor

from config import DP


async def get_rss(link: str) -> str:
    """
    Получение rss-ленты по ссылке

    Parameters
    ----------
    link : str
        Ссылка на rss-ленту

    Returns
    -------
    msg : str
        Распрашенная строка с постами и ссылками
    """

    d = feedparser.parse(link)

    msg = ''
    for i in d['entries']:
        msg += f'*{i["title"]}*\n'
        msg += f'[Ссылка]({i["link"]})\n\n'

    return msg


@DP.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """
    Обработка команды /start

    Parameters
    ----------
    message : aiogram.types.Message
        Объект сообщения
    """

    await message.reply(f'Привет, {message.chat.username}!')


@DP.message_handler(commands=['dtf'])
async def process_dtf_command(message: types.Message):
    """
    Обработка команды /dtf
    Получение постов с сайта dtf.ru

    Parameters
    ----------
    message : aiogram.types.Message
        Объект сообщения
    """

    msg = await get_rss('https://dtf.ru/rss')

    await message.answer(
        msg,
        parse_mode='markdown',
        disable_web_page_preview=True,
        disable_notification=True
    )


@DP.message_handler(commands=['habr'])
async def process_habr_command(message: types.Message):
    """
    Обработка команды /habr
    Получение постов с сайта habr.com

    Parameters
    ----------
    message : aiogram.types.Message
        Объект сообщения
    """

    msg = await get_rss('https://habr.com/ru/rss/all/all/?fl=ru')

    await message.answer(
        msg,
        parse_mode='markdown',
        disable_web_page_preview=True,
        disable_notification=True
    )


@DP.message_handler(commands=['weather'])
async def process_weather_command(message: types.Message):
    """
    Обработка команды /weather
    Получение текущей погоды

    Parameters
    ----------
    message : aiogram.types.Message
        Объект сообщения
    """

    key = os.environ.get('APP_ID')
    # Координаты Костромы
    lat = '57.767961'
    lon = '40.926858'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&lang=ru&units=metric'

    res = requests.get(url)
    res_json = res.json()

    temp = res_json.get('main').get('temp')
    pressure = int(res_json['main']['pressure'] * 0.750062)
    humidity = res_json.get('main').get('humidity')
    now = datetime.datetime.now().strftime('%w %b %Y  %H:%M')

    msg = f'{now}\n\n*Температура:* {temp}°C\n*Давление:* {pressure} мм рт ст\n*Влажность:* {humidity}%'

    await message.answer(
        msg,
        parse_mode='markdown',
        disable_web_page_preview=True,
        disable_notification=True
    )


@DP.message_handler(commands=['exchange'])
async def process_exchange_command(message: types.Message):
    """
    Обработка команды /exchange
    Получение текущего курса валют

    Parameters
    ----------
    message : aiogram.types.Message
        Объект сообщения
    """

    await message.reply(str(message))


if __name__ == '__main__':
    executor.start_polling(DP)
