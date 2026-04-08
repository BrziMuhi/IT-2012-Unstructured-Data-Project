import os
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter
import pytesseract
from pdf2image import convert_from_path

from utils.logger import logging


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\Library\bin"
POPPLER_PATH = r"C:\Users\hp\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"




def preprocess_image(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = gray.filter(ImageFilter.SHARPEN)
    bw = gray.point(lambda x: 0 if x < 150 else 255, "1")
    return bw

def ocr_image(image_path: str):
    try:
        logging.info(f"OCR image: {image_path}")
        image = Image.open(image_path)

        raw_text = pytesseract.image_to_string(image)

        processed_image = preprocess_image(image)
        processed_text = pytesseract.image_to_string(processed_image)

        return {
            "file_name": os.path.basename(image_path),
            "source": image_path,
            "type": "ocr_image",
            "raw_text": raw_text,
            "processed_text": processed_text,
            "extraction_timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logging.error(f"OCR image failed for {image_path}: {e}")
        return None

def ocr_scanned_pdf(pdf_path: str):
    try:
        logging.info(f"OCR scanned PDF: {pdf_path}")
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

        results = []

        for i, page in enumerate(pages, start=1):
            processed_page = preprocess_image(page)
            text = pytesseract.image_to_string(processed_page)

            results.append({
                "file_name": os.path.basename(pdf_path),
                "source": pdf_path,
                "type": "ocr_pdf",
                "page_number": i,
                "text": text,
                "extraction_timestamp": datetime.utcnow().isoformat()
            })

        return results

    except Exception as e:
        logging.error(f"OCR scanned PDF failed for {pdf_path}: {e}")
        return []