from pathlib import Path

import imagehash
from PIL import Image

from utils.image_core import PictureData

new = PictureData(
    path=Path("jpeg_data.jpeg"),
    phash=imagehash.phash(Image.open(str(Path("jpeg_data.jpeg")))),
)
