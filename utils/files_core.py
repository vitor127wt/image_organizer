from pathlib import Path

import imagehash
from PIL import Image, PngImagePlugin

from utils.image_core import PictureData

from .xml_template_generator import generate_xml_template


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


def save_picture(
    picture: PictureData,
    *,
    file_extension: str | None = None,
    tags_path: bool = True,
    insert_tags: bool = True,
) -> None:

    if not file_extension:
        file_extension = picture.suffix
    else:
        file_extension = (
            f".{file_extension}".lower()
            if "." not in file_extension
            else file_extension.lower()
        )

    if tags_path:
        path = picture.new_path.with_suffix(file_extension)
    else:
        path = picture.path.with_suffix(file_extension)

    path.parent.mkdir(parents=True, exist_ok=True)

    if not insert_tags:
        with Image.open(picture.path) as img:
            if not path.exists():
                img.save(path)
                return

            file_iter = 1
            while True:
                new_file_name = path.stem + f"_{file_iter}" + file_extension
                new_path = path.parent / new_file_name

                if not new_path.exists():
                    img.save(new_path)
                    return

                file_iter += 1

    xml, xml_bytes = (
        generate_xml_template(picture.tags, encode=False),
        generate_xml_template(picture.tags),
    )

    with Image.open(picture.path) as img:
        new_data = img.info.copy()
        try:
            if file_extension in (".jpg", ".jpeg") and img.mode in (
                "RGBA",
                "LA",
                "P",
            ):
                white_background = Image.new("RGB", img.size, (255, 255, 255))

                if img.mode == "P":
                    white_background.paste(
                        img.convert("RGBA"), mask=img.convert("RGBA").split()[3]
                    )
                else:
                    white_background.paste(img, mask=img.split()[3])

                final_image = white_background
            else:
                final_image = img

            if file_extension in (".jpg", ".jpeg", ".webp"):
                new_data["xmp"] = xml_bytes

                final_image.save(path, xmp=xml_bytes, **new_data)  # type: ignore
            elif file_extension == ".png":
                meta_png = PngImagePlugin.PngInfo()

                for key, value in new_data.items():
                    if isinstance(value, str):
                        meta_png.add_text(key, value)  # type: ignore

                meta_png.add_itxt("XML:com.adobe.xmp", xml)

                final_image.save(path, pnginfo=meta_png)

            elif file_extension in (".tiff", ".tif"):
                if "tiffinfo" in new_data:
                    new_data["tiffinfo"] = xml_bytes

                final_image.save(path, **new_data)  # type: ignore

            else:
                final_image.save(path)

            return
        except Exception as e:
            print(f"Error saving image with metadata: {e}")
            return None
