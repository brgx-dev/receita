import zipfile

from scripts.config import EXTRACTION_DIRECTORY
from .logging_utils import log_extraction

def unzip_data(zip_file_path: str):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACTION_DIRECTORY)
    log_extraction(zip_file_path)
