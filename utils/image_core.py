import re
from dataclasses import dataclass, field
from pathlib import Path

import imagehash
from PIL import Image

from .tags_core import Tag


@dataclass()
class PictureData:
    path: Path
    phash: imagehash.ImageHash
    to_suffix: str = ""
    _tags: list[Tag] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._sufix = self.path.suffix.replace(".", "")
        self._size_bytes = self.path.stat().st_size

    @property
    def suffix(self) -> str:
        return self._sufix

    @property
    def size(self) -> int:
        return self._size_bytes

    @property
    def tags(self) -> list[Tag]:
        return sorted(self._tags, key=lambda n: n.nivel)

    @property
    def new_path(self):
        new_path = (
            Path(self.path.parent)
            / "/".join(
                [valores.nome for valores in self.tags],
            )
            / self.path.name
        )
        return new_path

    @property
    def get_metadata(self) -> None | list[str] | list:
        try:
            raw_xmp = Image.open(str(self.path)).info.get("xmp")
        except Exception as e:
            print(e)
            raw_xmp = None
            return raw_xmp

        if raw_xmp is not None:
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

                return cleaned_tags

            tags_xml_windows_block = re.search(
                r"<MicrosoftPhoto:LastKeywordXMP>(.*?)</MicrosoftPhoto:LastKeywordXMP>",
                xml_text,
                re.DOTALL,
            )
            if tags_xml_windows_block:
                tags_xml = tags_xml_windows_block.group(1)
                tags = re.findall(r"<rdf:li>(.*?)</rdf:li>", tags_xml)
                cleaned_tags = [tag.strip() for tag in tags if tag.strip()]

                return cleaned_tags

        return []


if __name__ == "__main__":
    pass
