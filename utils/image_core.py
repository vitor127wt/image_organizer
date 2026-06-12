from dataclasses import dataclass, field
from pathlib import Path

import imagehash
from PIL import Image

from utils.tags_core import Tag


@dataclass()
class PictureData:
    path: Path
    phash: imagehash.ImageHash
    tags: list[Tag] = field(default_factory=list)

    def __post_init__(self, *args, **kwargs) -> None:
        self._sufix = self.path.suffix.replace(".", "")
        self._size_bytes = self.path.stat().st_size

    @property
    def suffix(self) -> str:
        return self._sufix

    @property
    def size(self) -> int:
        return self._size_bytes

    @classmethod
    def get_pictures(cls, folder: Path) -> list:
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
