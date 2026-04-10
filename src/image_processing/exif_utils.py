from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def extract_exif(path):
    img = Image.open(path)
    exif_data = img.getexif()

    if not exif_data:
        return {}

    exif = {}
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)

        if tag == "GPSInfo" and isinstance(value, dict):
            gps_data = {}
            for gps_key, gps_value in value.items():
                decoded_key = GPSTAGS.get(gps_key, gps_key)
                gps_data[decoded_key] = gps_value
            exif[tag] = gps_data
        else:
            exif[tag] = value

    return exif


def extract_gps(exif):
    gps_info = exif.get("GPSInfo")

    if not gps_info or not isinstance(gps_info, dict):
        return None

    gps_data = {}
    for key, value in gps_info.items():
        decoded = GPSTAGS.get(key, key)
        gps_data[decoded] = value

    return gps_data


def get_exif_summary(path):
    exif = extract_exif(path)
    gps = extract_gps(exif)

    summary = {
        "camera_make": exif.get("Make"),
        "camera_model": exif.get("Model"),
        "datetime_original": exif.get("DateTimeOriginal") or exif.get("DateTime"),
        "lens_model": exif.get("LensModel"),
        "iso": exif.get("ISOSpeedRatings"),
        "focal_length": exif.get("FocalLength"),
        "gps": gps
    }

    return summary


def save_without_exif(input_path, output_path):
    img = Image.open(input_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    data = list(img.getdata())
    clean_img = Image.new(img.mode, img.size)
    clean_img.putdata(data)
    clean_img.save(output_path)

    return output_path