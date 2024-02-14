# DXEMONLOAD Bot v0.1.0
# Copyright ©️ Tim Nagorskikh, 2024
# Original: https://github.com/trvedxemon/dxemonloadbot
# Preview: https://t.me/dxemonloadbot
# ------------------------------------
#               BASICS
# ------------------------------------
# Written in Python 3 using aiogram v3.1, ffmpeg-python v0.2.0 and pytube v15.0
# config.py - constants and details
# ytloader.py - main worker
# /tmp - default folder for loading files from YouTube
# /tmp/merged - folder for processed videos
# ------------------------------------
#            INSTALLATION
# ------------------------------------
# - Create bot via BotFather, then add API Token to config.py instead of placeholder
# - Install libraries:
# - - pip install aiogram
# - - pip install pytube
# - - pip install ffmpeg-python
# - Run the bot.py
# ------------------------------------
#            OTHER INFO
# ------------------------------------
# 1. Video and audio files by default are saved to /tmp. If necessary, change the 'filepath' var in config.py
# 2. Bot uses long-polling by default. If you know what webhook is, you can rewrite it to use them instead
# 3. Downloaded files are deleted soon, but keep an eye on the folder's size, there's no in-built control


import asyncio
import logging
import os
import sys
import string
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery, URLInputFile

from config import API_TOKEN, infomsg, filepath
from ytloader import get_yt_name, get_yt_img, get_yt_res, ytdownloadaudio, ytdownloadvid

bot = Bot(API_TOKEN)
dp = Dispatcher()
rt = Router()
link: string
msg: Message


@dp.callback_query()
async def callback_handler(call: CallbackQuery):
    callb = str(call.data)
    callb = callb.split("-/")
    link = callb[0]
    itag = callb[1]
    type = callb[2]
    usid = call.from_user.id
    if type == "video":
        audio = callb[3]
        await call.answer()
        await bot.send_message(chat_id=usid, text="Downloading video, please wait...")
        path = ytdownloadvid(link, itag, audio)
        vid = FSInputFile(path)
        await bot.send_video(usid, vid)
        os.remove(path)
    elif type == "audio":
        await call.answer()
        await bot.send_message(chat_id=usid, text="Downloading audio, please wait...")
        filename = ytdownloadaudio(link, itag)
        path = filepath + filename
        aud = FSInputFile(path)
        await bot.send_audio(usid, aud)
        os.remove(path)



@dp.message(CommandStart())
async def command_handler(message: Message) -> None:
    name = message.from_user.first_name
    await message.answer("""Hello, """ + name + """!""")
    await asyncio.sleep(.2)
    await message.answer(infomsg, parse_mode='MarkdownV2')


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(infomsg, parse_mode='MarkdownV2')


@dp.message()
async def command_help_handler(message: Message) -> None:
    thumbnail = URLInputFile(get_yt_img(message.text))
    usid = message.from_user.id
    name = get_yt_name(message.text)
    kb = get_yt_res(message.text)
    await message.answer_photo(thumbnail, name, reply_markup=kb)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
