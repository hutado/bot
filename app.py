import feedparser

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hi")


@dp.message_handler(commands=['dtf'])
async def dtf_rss_command(message: types.Message):
    rss_link = 'https://dtf.ru/rss'
    d = feedparser.parse(rss_link)
    msg = ''
    for i in d['entries']:
        msg += f"*{i['title']}*\n"
        msg += f"[Ссылка]({i['link']})\n\n"

    await message.answer(
        msg,
        parse_mode='markdown',
        disable_web_page_preview=True,
        disable_notification=True
    )


@dp.message_handler(commands=['habr'])
async def habr_rss_command(message: types.Message):
    rss_link = 'https://habr.com/ru/rss/all/all/?fl=ru'
    d = feedparser.parse(rss_link)

    msg = ''
    for i in d['entries']:
        msg += f"*{i['title']}*\n"
        msg += f"[Ссылка]({i['link']})\n\n"

    await message.answer(
        msg,
        parse_mode='markdown',
        disable_web_page_preview=True,
        disable_notification=True
    )


if __name__ == '__main__':
    executor.start_polling(dp)
