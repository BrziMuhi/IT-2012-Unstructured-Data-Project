import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.storage.drive import upload_file

file = "data/processed/webp/iGpMm603GUKH2SiXB2S5m4sZ17t.webp"

upload_file(file)