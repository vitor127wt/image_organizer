import json
from pathlib import Path

import imagehash
from PIL import Image

from utils.files_core import save_picture
from utils.image_core import PictureData
from utils.tags_core import TagsList

tipo = "png"
picture_path = Path(f"{tipo}_no_data.{tipo}")

new_picture = PictureData(
    path=picture_path, phash=imagehash.phash(Image.open(picture_path))
)


new_picture.add_tag(TagsList.Lolis)
new_picture.add_tag(TagsList.Imagem)
new_picture.add_tag(TagsList.NIRL)

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(new_picture.tags, f)


print(new_picture.tags)

save_picture(new_picture)
