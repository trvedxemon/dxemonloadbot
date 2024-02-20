import os

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytube import YouTube
import ffmpeg
from pytube.exceptions import AgeRestrictedError

from config import filepath, merged_filepath


def ytdownloadvid(link, itag, audio):
    ytobject = YouTube(link)
    video = ytobject.streams.get_by_itag(itag)
    audio = ytobject.streams.get_by_itag(audio)
    try:
        video.download(output_path=filepath)
        audio.download(output_path=filepath)
        filename1 = filepath + video.default_filename
        filename2 = filepath + video.default_filename
        out = merged_filepath + video.default_filename
        video = ffmpeg.input(filename1)
        audio = ffmpeg.input(filename2)
        ffmpeg.concat(video, audio, v=1, a=1).output(out).run()
        os.remove(filename1)
        os.remove(filename2)
    except AgeRestrictedError:
        return "Age restricted"
    except:
        return "Nothing"
    return out


def ytdownloadaudio(link, itag):
    ytobject = YouTube(link)
    ytobject = ytobject.streams.get_by_itag(itag)
    try:
        ytobject.download(output_path=filepath)
        filename = ytobject.default_filename
    except:
        return "Nothing"
    return filename


def get_yt_img(link):
    yt = YouTube(link)
    for stream in yt.streams:
        print(stream)
    img = yt.thumbnail_url
    return img


def get_yt_name(link):
    yt = YouTube(link)
    name = yt.title
    return name


def get_yt_res(link):
    yt = YouTube(link)
    builder = InlineKeyboardBuilder()
    for stream in yt.streams.order_by('resolution').filter(file_extension='mp4', adaptive=True).desc():
        audio = yt.streams.filter(mime_type="audio/webm").order_by('abr').desc().first()
        fs = stream.filesize_mb + audio.filesize_mb
        audio = str(audio.itag)
        if fs < 50:
            btnname = "Video " + stream.resolution + str(stream.fps) + " | " + str(round(fs, 2)) + " MB"
            callback = link + "-/" + str(stream.itag) + "-/video-/" + audio
            btn = InlineKeyboardBuilder()
            btn.row(InlineKeyboardButton(text=btnname, callback_data=callback))
            builder.attach(btn)
    for stream in yt.streams.filter(mime_type="audio/webm").order_by('abr').desc():
        if stream.filesize_mb < 50:
            btnname = "Audio " + stream.abr + " | " + str(round(stream.filesize_mb, 2)) + " MB"
            audio = str(stream.itag)
            callback = link + "-/" + audio + "-/audio"
            btn = InlineKeyboardBuilder()
            btn.row(InlineKeyboardButton(text=btnname, callback_data=callback))
            builder.attach(btn)
    return builder.as_markup()


def get_yt_shorts(link):
    yt = YouTube(link)
    yt = yt.streams.get_highest_resolution()
    name = yt.default_filename
    try:
        yt.download(output_path=filepath)
    except:
        print("An error has occurred")
    return name