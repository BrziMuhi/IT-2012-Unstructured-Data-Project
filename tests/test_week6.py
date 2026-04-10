import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.image_processing.processor import *

from src.image_processing.exif_utils import (
    extract_exif,
    get_exif_summary,
    save_without_exif
)

img = "data/raw/images/iGpMm603GUKH2SiXB2S5m4sZ17t.jpg"

print("\n--- INSPECT ---")
print(inspect_image(img))

print("\n--- RESIZE ---")
resize_image(img, "data/processed/resized/fixed.jpg", 300, 450)
resize_proportional(img, "data/processed/resized/proportional.jpg", max_width=300)

print("\n--- THUMBNAILS ---")
generate_thumbnail(img, "data/processed/thumbnails/thumb.jpg")
generate_fixed_thumbnail(img, "data/processed/thumbnails/fixed_thumb.jpg")

print("\n--- CROP ---")
crop_image(img, "data/processed/cropped/top.jpg", (0, 0, 342, 200))
crop_center_square(img, "data/processed/cropped/square.jpg")

print("\n--- CONVERSION ---")
convert_to_webp(img, "data/processed/webp/poster.webp")
convert_to_grayscale(img, "data/processed/gray/poster_gray.jpg")
save_optimised_jpeg(img, "data/processed/jpeg/poster_opt.jpg")

print("\n--- FILTERS ---")
apply_blur(img, "data/processed/filters/blur.jpg", radius=3)
apply_sharpen(img, "data/processed/filters/sharpen.jpg")
apply_edge_detection(img, "data/processed/filters/edges.jpg")

enhance_contrast(img, "data/processed/filters/contrast.jpg")
enhance_brightness(img, "data/processed/filters/brightness.jpg")
enhance_color(img, "data/processed/filters/color.jpg")


print("\n--- EXIF ---")

images = [
    "data/raw/exif_samples/exif_sample1.jpg",
    "data/raw/exif_samples/exif_sample2.jpg"
]

for exif_img in images:
    print(f"\n--- Processing: {exif_img} ---")

    print("\nFULL EXIF:")
    print(extract_exif(exif_img))

    print("\nSUMMARY:")
    print(get_exif_summary(exif_img))

    print("\nSAVE CLEAN COPY:")
    save_without_exif(
        exif_img,
        f"data/processed/exif_clean/{os.path.basename(exif_img)}"
    )

print("\n--- DONE ---")