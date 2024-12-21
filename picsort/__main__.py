from argparse import ArgumentParser
from pathlib import Path

from .picsort import Sorter


def main():
    """establish context"""
    parser = ArgumentParser(
        prog="picsort",
        description="Neatly sort your images into folders. By default, images are copied not moved",
    )
    parser.add_argument("source", help="Where images are from.")
    parser.add_argument("target", help="Where images should go.")
    parser.add_argument(
        "--move", action="store_true", help="If set files are moved not copied."
    )
    args = parser.parse_args()

    if args.move:
        print("Files will be moved")
        sorter = Sorter(Path(args.source), Path(args.target), move=True)
    else:
        print("Files will be copied")
        sorter = Sorter(Path(args.source), Path(args.target))

    sorter.run()
