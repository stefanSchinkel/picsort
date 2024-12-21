"""picsort.py
Move images to dedicated folders based on Exif info or filename
"""
import logging
from datetime import datetime as dt
from os import getenv, rename
from pathlib import Path
from shutil import copy
from uuid import uuid1

from PIL import Image, UnidentifiedImageError


class FileNotFoundError(Exception):
    pass


class SourceNotFoundError(Exception):
    pass


class TargetNotFoundError(Exception):
    pass


class Sorter:
    """Sorting and exif are separate, just for better testing"""

    def __init__(self, source: Path, target: Path, move: bool = False):
        self.logger = logging.getLogger(__name__)
        lvl = getenv("LOGLEVEL", "INFO")
        logging.basicConfig(format="%(levelname)s:%(message)s", level=lvl)

        if not source.exists():
            self.logger.error("source directory does not exist")
            raise SourceNotFoundError

        if not target.exists():
            self.logger.error("target directory does not exist")
            raise TargetNotFoundError

        self.src: Path = source
        self.tgt: Path = target
        self.move = move
        self.files = [x for x in self.src.rglob("*") if x.is_file()]

    def run(self):
        """Does the actual stuff"""
        # feed to Exifreader
        for f in self.files:
            try:
                er = ExifReader(f)
            except FileNotFoundError:
                self.logger.info(f"{f} is not present or not an image")
                continue

            if not er.proc():
                self.logger.info(f"{f} has no exif data")
                continue

            self.move_files(f, er.tgt)

    def move_files(self, src: Path, tgt: Path):
        """move or copy file"""

        tgt = Path.joinpath(self.tgt, tgt)
        tgt.parent.mkdir(parents=True, exist_ok=True)

        if self.move:
            logging.debug(
                f"Will move {src.absolute()} to {tgt.absolute()} creating {tgt.parent}."
            )
            rename(src, tgt)
        else:
            logging.debug(
                f"Will copy {src.absolute()} to {tgt.absolute()} creating {tgt.parent}."
            )
            copy(src, tgt)


class ExifReader:
    """Reads an image file and assembles a path and filename"""

    def __init__(self, src_file: Path) -> None:
        self.src_file = src_file
        self.ext = self.src_file.suffix
        self.tgt: Path

        try:
            self.pimg = Image.open(self.src_file)
        except (IOError, UnidentifiedImageError):
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
