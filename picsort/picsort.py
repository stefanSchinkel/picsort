"""picsort.py
Move images to dedicated folders based on Exif info or filename
"""

from datetime import datetime as dt
from pathlib import Path
from uuid import uuid1

from PIL import Image


class FileNotFoundError(Exception):
    pass


class ExifReader:
    """Reads an image file and assembles a path and filename"""

    def __init__(self, src_file: Path) -> None:
        self.src_file = src_file
        self.ext = self.src_file.suffix
        self.tgt: Path

        try:
            self.pimg = Image.open(self.src_file)
        except IOError:
            raise FileNotFoundError

    def proc(self) -> bool:
        """Main routine"""
        fmt = "%Y:%m:%d %H:%M:%S"
        f_format = "%Y-%m-%d %H-%M-%S"

        self.exif = self.pimg.getexif()

        try:
            self.ts = self.exif[306]
            self.dt = dt.strptime(self.ts, fmt)
        except KeyError:
            return False

        p = self.dt.strftime("%Y/%m/")
        self.tgt = Path(f"{p}{self.dt.strftime(f_format)} {str(uuid1())[:4]}{self.ext}")

        return True
