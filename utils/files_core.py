from pathlib import Path

import imagehash
from PIL import Image

from utils.image_core import PictureData


def get_pictures(folder: Path) -> list:
    permitted_suffixes: tuple = (
        ".png",
        ".jpg",
        ".webp",
        ".jpeg",
        ".gif",
        ".btm",
    )
    pictures: list[PictureData] = []
    for file in folder.iterdir():
        if not file.is_file() or file.suffix not in permitted_suffixes:
            continue

        new_picture = PictureData(
            path=file, phash=imagehash.phash(Image.open(file))
        )

        pictures.append(new_picture)

    return pictures
