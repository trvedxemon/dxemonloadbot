DXEMONLOAD Bot v0.1.0

Copyright ©️ Tim Nagorskikh, 2024

Original: https://github.com/trvedxemon/dxemonloadbot

Preview: https://t.me/dxemonloadbot

------------------------------------
              BASICS
------------------------------------
Written in Python 3 using aiogram v3.1, ffmpeg-python v0.2.0 and pytube v15.0

config.py - constants and details

ytloader.py - main worker

/tmp - default folder for loading files from YouTube

/tmp/merged - folder for processed videos

------------------------------------
            INSTALLATION
 ------------------------------------
 - Create bot via BotFather, then add API Token to config.py instead of placeholder
 - Install libraries:
 - - pip install aiogram
 - - pip install pytube
 - - pip install ffmpeg-python
 - Run the bot.py
 ------------------------------------
            OTHER INFO
 ------------------------------------
 1. Video and audio files by default are saved to /tmp. If necessary, change the 'filepath' var in config.py
 2. Bot uses long-polling by default. If you know what webhook is, you can rewrite it to use them instead
 3. Downloaded files are deleted soon, but keep an eye on the folder's size, there's no in-built control
