"""Tests for the exif reader
"""

from pathlib import Path

import pytest

from picsort.picsort import ExifReader, FileNotFoundError


def test_init_fail():
    """make sure we dont do shite"""
    # Arrange
    fname = Path("/home/i/do/not/exist.png")
    # Act

    # Assert
    with pytest.raises(FileNotFoundError):
        ExifReader(fname)


def test_no_image():
    """make sure we raise if file is not an image"""
    # Arrange
    fname = Path("./tests/test_basic.py")
    # Act

    # Assert
    with pytest.raises(FileNotFoundError):
        ExifReader(fname)


def test_exif_fail():
    """raise error when no exif found"""
    # Arrange
    fname = Path("./tests/pillow_noexif.png")

    # Act
    er = ExifReader(fname)

    # Assert
    assert er.proc() is False


def test_parse_success():
    """Make sure all is filled correctly"""
    # Arrange
    fname = Path("./tests/pillow.png")
    expected = "2024/12/2024-12-21 12-51-08"

    # Act
    er = ExifReader(fname)

    # Assert
    assert er.proc() is True
    assert str(er.tgt).startswith(expected)
