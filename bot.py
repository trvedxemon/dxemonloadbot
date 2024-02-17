# DXEMONLOAD Bot v0.1.2
# Copyright ©️ Tim Nagorskikh, 2024
# Original: https://github.com/trvedxemon/dxemonloadbot
# Preview: https://t.me/dxemonloadbot
# ------------------------------------
#               BASICS
# ------------------------------------
# Written in Python 3 using aiogram 3.1, ffmpeg-python 0.2.0, pydub 0.25.1 and pytube 15.0
# config.py - constants and details
# ytloader.py - main worker
# muscoder.py - music transcoder
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
# - - pip install pydub
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
from muscoder import rebuild_webm
from ytloader import get_yt_name, get_yt_img, get_yt_res, ytdownloadaudio, ytdownloadvid, get_yt_shorts

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
        await bot.send_video(usid, vid, caption=f"[original]({link}) \| [via](https://t.me/dxemonloadbot)", parse_mode='MarkdownV2')
        os.remove(path)
    elif type == "audio":
        await call.answer()
        await bot.send_message(chat_id=usid, text="Downloading audio, please wait...")
        filename = ytdownloadaudio(link, itag)
        path = filepath + filename
        path = rebuild_webm(path)
        aud = FSInputFile(path)
        await bot.send_audio(usid, aud, caption=f"[original]({link}) \| [via](https://t.me/dxemonloadbot)", parse_mode='MarkdownV2')
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
    if "instagram" in message.text:
        await message.answer("Sorry, Instagram is not yet supported 🙁")
    elif "youtu" in message.text:
        if "?si=" in message.text:
            msgtext = message.text.split("?si=")
            msgtext = msgtext[0]
        elif "&list=" in message.text:
            msgtext = message.text.split("&list=")
            msgtext = msgtext[0]
        else:
            msgtext = message.text
        thumbnail = URLInputFile(get_yt_img(msgtext))
        usid = message.from_user.id
        name = get_yt_name(msgtext)
        kb = get_yt_res(msgtext)
        await message.answer_photo(thumbnail, name, reply_markup=kb)
    else:
        await message.answer("Sorry, the link is not supported 🙁")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
