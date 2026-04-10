import os
from pathlib import Path
from tqdm import tqdm

from src.image_processing.processor import (
    resize_image,
    generate_thumbnail,
    convert_to_webp,
    inspect_image
)
from src.storage.mongo import save_image_metadata


def process_single(image_path):
    filename = Path(image_path).stem

    resized_path = f"data/processed/resized/{filename}_resized.jpg"
    thumb_path = f"data/processed/thumbnails/{filename}_thumb.jpg"
    webp_path = f"data/processed/webp/{filename}.webp"

    resize_image(image_path, resized_path, 300, 450)
    generate_thumbnail(image_path, thumb_path)
    convert_to_webp(image_path, webp_path)

    info = inspect_image(image_path)

    metadata = {
        "filename": filename,
        "original_path": image_path,
        "resized_path": resized_path,
        "thumbnail_path": thumb_path,
        "webp_path": webp_path,
        "format": info["format"],
        "width": info["width"],
        "height": info["height"],
        "file_size_kb": info["file_size_kb"]
    }

    save_image_metadata(metadata)


def batch_process_images(folder="data/raw/images"):
    images = [f for f in os.listdir(folder) if f.endswith(".jpg")]

    for img in tqdm(images, desc="Processing images"):
        path = os.path.join(folder, img)

        try:
            process_single(path)
        except Exception as e:
            print(f"Error processing {img}: {e}")