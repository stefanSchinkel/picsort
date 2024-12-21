"""Tests for the exif reader
"""

from pathlib import Path

import pytest

from picsort.picsort import ExifReader, ExifNotFoundError, FileNotFoundError


def test_init_fail():
    """make sure we dont do shite"""
    # Arrange
    fname = Path("/home/i/do/not/exist.png")
    # Act

    # Assert
    with pytest.raises(FileNotFoundError):
        er = ExifReader(fname)


def test_exif_fail():
    """raise error when no exif found"""
    # Arrange
    fname = Path("./tests/pillow_noexif.png")

    # Act
    er = ExifReader(fname)

    # Assert
    with pytest.raises(ExifNotFoundError):
        er.proc()
