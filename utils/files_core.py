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
    replace: bool = False,
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

    xml = generate_xml_template(picture.tags, encode=False)
    with open("tag.xml", "w", encoding="utf-8") as f:
        f.write(str(xml))

    xml_bytes = generate_xml_template(picture.tags)

    with Image.open(picture.path) as img:
        if path == picture.path and not replace:
            file_iter = 1
            while True:
                new_file_name = path.stem + f"_{file_iter}" + file_extension
                new_path = path.parent / new_file_name

                if not new_path.exists():
                    path = new_path
                    break
                file_iter += 1

        new_data = img.info.copy()
        if file_extension in (".jpg", ".jpeg") and img.mode in (
            "RGBA",
            "LA",
            "P",
        ):
            white_background = Image.new("RGB", img.size, (255, 255, 255))
            img_rgba = img.convert("RGBA")
            white_background.paste(img_rgba, mask=img_rgba.split()[3])
            final_image = white_background
        else:
            final_image = img if not replace else img.copy()

    try:
        if file_extension in (".jpg", ".jpeg", ".webp"):
            new_data.pop("exif", None)
            new_data["xmp"] = xml_bytes

            final_image.save(path, xmp=new_data["xmp"])  # type: ignore
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

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Error saving image with metadata: {e}")
        return None
    return
