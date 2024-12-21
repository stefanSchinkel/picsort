"""Tests for the exif reader
"""

import logging
import os
import shutil
from pathlib import Path

import pytest

from picsort.picsort import Sorter, SourceNotFoundError, TargetNotFoundError


def test_init_src_not_existing(caplog):
    """Fail hard w/ out source"""
    # Arrange
    src = Path("/home/i/do/not/exist/")
    tgt = Path("/home/i/do/not/exist/either")
    # Act

    # Assert
    with pytest.raises(SourceNotFoundError):
        Sorter(src, tgt)
    assert "source directory does not exist" in caplog.text


def test_init_tgt_not_existing(caplog):
    """Fail hard w/ out target"""
    # Arrange
    src = Path("./tests/imgs/")
    tgt = Path("/home/i/do/not/exist/either")
    # Act

    # Assert
    with pytest.raises(TargetNotFoundError):
        Sorter(src, tgt)
    assert "target directory does not exist" in caplog.text


def test_log_on_no_img(caplog, tmp_path):
    """just make sure none images get logged"""
    # Arrange
    src = tmp_path / "in"
    src.mkdir()
    tgt = tmp_path / "out"
    tgt.mkdir()

    s = Sorter(src, tgt)
    s.files = [Path("./tests/__init__.py")]
    # Act

    # Assert
    with caplog.at_level(logging.INFO):
        s.run()
        assert "is not present or not an image" in caplog.text


def test_log_on_no_exif(caplog, tmp_path):
    """just make sure none images get logged"""
    # Arrange
    src = tmp_path / "in"
    src.mkdir()
    tgt = tmp_path / "out"
    tgt.mkdir()

    # Act
    s = Sorter(src, tgt)
    s.files = [Path("./tests/imgs/pillow_noexif.png")]

    # Assert
    with caplog.at_level(logging.INFO):
        s.run()
        assert "has no exif data" in caplog.text


def test_copy(tmp_path):
    """check if move moves"""
    # Arrange
    src = Path("./tests/imgs/")
    tgt = tmp_path / "out"
    tgt.mkdir()
    check_dir = tgt / "2024/11"
    # Act
    s = Sorter(src, tgt)
    s.run()
    files = os.listdir(check_dir)

    # Assert
    assert len(files) == 2
    assert len(os.listdir(src)) == 5


def test_move(tmp_path):
    """just make sure none images get logged"""
    # Arrange
    src = tmp_path / "in"
    src.mkdir()
    tgt = tmp_path / "out"
    tgt.mkdir()
    shutil.copy("./tests/imgs/pillow.png", src)
    shutil.copy("./tests/imgs/pillow_noexif.png", src)

    # Act
    s = Sorter(src, tgt, move=True)
    s.run()

    # Assert
    assert len(os.listdir(tgt)) == 1  # one should move
    assert len(os.listdir(src)) == 1  # and one should stay
