import re
from dataclasses import dataclass, field
from pathlib import Path

import imagehash
from PIL import Image

from .tags_core import Tag, TagsList


@dataclass
class PictureData:
    path: Path
    phash: imagehash.ImageHash
    _tags: list[Tag] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._sufix = self.path.suffix
        self._size_bytes = self.path.stat().st_size
        self.__metadata()

    @property
    def suffix(self) -> str:
        return self._sufix

    @property
    def size(self) -> int:
        return self._size_bytes

    @property
    def tags(self) -> list[Tag]:
        return sorted(self._tags, key=lambda n: n.nivel)

    @tags.deleter
    def tags(self) -> None:
        self._tags.clear()

    def add_tag(self, tag: Tag) -> None:
        self._tags.append(tag)

    def delete_tag(self, name: str) -> None:
        self._tags = [tag for tag in self._tags if tag.nome != name]

    @property
    def new_path(self) -> Path:
        absolute_path = self.path.resolve()
        new_path = (
            Path(absolute_path.parent)
            / "/".join([valores.nome for valores in self.tags])
            / self.path.name
        )
        return new_path

    def __metadata(self) -> list[Tag]:
        try:
            raw_xmp = Image.open(str(self.path)).info.get("xmp")
        except Exception as e:
            print(e)
            raw_xmp = None
            # TODO: Add logging

        if raw_xmp is None:
            return self.tags

        xml_text = (
            raw_xmp.decode("utf-8", errors="ignore")
            if isinstance(raw_xmp, bytes)
            else str(raw_xmp)
        )

        tags_xml_digikam_block = re.search(
            r"<digiKam:TagsList>(.*?)</digiKam:TagsList>",
            xml_text,
            re.DOTALL,
        )

        if tags_xml_digikam_block:
            tags_xml = tags_xml_digikam_block.group(1)

            tags = re.findall(r"<rdf:li>(.*?)</rdf:li>", tags_xml)

            cleaned_tags = [tag.strip() for tag in tags if tag.strip()]

            # TODO: Add logging.

            for tag in cleaned_tags:
                if tag in list(TagsList.__dict__.keys()):
                    self._tags.append(TagsList.get_tag(tag))
                else:
                    self._tags.append(TagsList.Unknown)

            return self.tags

        tags_xml_windows_block = re.search(
            r"<MicrosoftPhoto:LastKeywordXMP>(.*?)</MicrosoftPhoto:LastKeywordXMP>",
            xml_text,
            re.DOTALL,
        )
        if tags_xml_windows_block:
            tags_xml = tags_xml_windows_block.group(1)
            tags = re.findall(r"<rdf:li>(.*?)</rdf:li>", tags_xml)
            cleaned_tags = [tag.strip() for tag in tags if tag.strip()]

            # TODO: Add logging.

            for tag in cleaned_tags:
                if tag in list(TagsList.__dict__.keys()):
                    self._tags.append(TagsList.get_tag(tag))
                else:
                    self._tags.append(TagsList.Unknown)

            return self.tags

        # TODO: Add logging.
        return self.tags


if __name__ == "__main__":
    pass
