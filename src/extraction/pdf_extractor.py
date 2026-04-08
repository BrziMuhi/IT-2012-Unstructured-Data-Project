import pdfplumber
from datetime import datetime
import logging

def extract_pdf(file_path):
    results = []

    try:
        with pdfplumber.open(file_path) as pdf:
            logging.info(f"Opened PDF: {file_path}")

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()

                # Extract tables
                tables = page.extract_tables()

                # FIX for None text
                if text is None:
                    text = ""

                results.append({
                    "content": text,
                    "tables": tables,
                    "metadata": {
                        "file_name": file_path,
                        "page": i + 1,
                        "document_type": "pdf",
                        "extraction_date": datetime.utcnow()
                    }
                })

    except Exception as e:
        logging.error(f"Error processing PDF {file_path}: {e}")

    return results