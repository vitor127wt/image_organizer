from dataclasses import dataclass, field
from pathlib import Path

import imagehash

from utils.tags_core import Tag


@dataclass()
class PictureData:
    path: Path
    phash: imagehash.ImageHash
    _tags: list[Tag] = field(default_factory=list)

    def __post_init__(self, *args, **kwargs) -> None:
        self._sufix = self.path.suffix.replace(".", "")
        self._size_bytes = self.path.stat().st_size

    @property
    def suffix(self) -> str:
        return self._sufix

    @property
    def size(self) -> int:
        return self._size_bytes

    @property
    def tags(self):
        return sorted(self._tags, key=lambda n: n.nivel)
