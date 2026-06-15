import json
from pathlib import Path

import imagehash
from PIL import Image

from utils.image_core import PictureData

picture_path = Path("png_data.png")

new_picture = PictureData(
    path=picture_path, phash=imagehash.phash(Image.open(picture_path))
)

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(new_picture.tags, f)


print(new_picture.new_path)
