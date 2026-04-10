import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.image_processing.batch import batch_process_images

batch_process_images()