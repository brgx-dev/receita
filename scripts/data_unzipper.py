import zipfile
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def unzip_data():
    download_directory = os.path.join(os.path.dirname(__file__), '../' + os.getenv("DOWNLOAD_DIRECTORY"))  # Read from .env
    EXTRACTION_DIRECTORY = os.path.join(os.path.dirname(__file__), '../' + os.getenv("EXTRACTION_DIRECTORY"))  # Read from .env
    for zip_file in os.listdir(download_directory):
        if zip_file.endswith('.zip'):
            zip_file_path = os.path.join(download_directory, zip_file)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(EXTRACTION_DIRECTORY)
    print("Unzipped to {}".format(EXTRACTION_DIRECTORY))
