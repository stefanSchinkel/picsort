"""picsort.py
Move images to dedicated folders based on Exif info or filename
"""

from pathlib import Path

from PIL import Image


class FileNotFoundError(Exception):
    pass


class ExifNotFoundError(Exception):
    pass


class ExifReader:
    def __init__(self, src_file: Path) -> None:
        self.src_file = src_file

        try:
            self.pimg = Image.open(self.src_file)
        except IOError:
            raise FileNotFoundError

    def proc(self) -> None:
        self.exif = self.pimg.getexif()
        try:
            self.ts = self.exif[306]
        except KeyError:
            raise ExifNotFoundError
