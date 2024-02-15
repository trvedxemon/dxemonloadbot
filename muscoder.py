import os

from pydub import AudioSegment


def rebuild_webm(path):
    song = AudioSegment.from_file(path)
    newname = path.split(".")
    songname = newname[0].split("/")
    songname = songname[1]
    newname = newname[0] + ".mp3"
    song.export(newname, format="mp3",
            tags={'title': songname})
    os.remove(path)
    return newname
