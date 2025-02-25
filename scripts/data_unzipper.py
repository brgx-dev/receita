import zipfile

def unzip_data(zip_file_path):
    from scripts.config import EXTRACTION_DIRECTORY
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACTION_DIRECTORY)
    print("Unzipped to {}".format(EXTRACTION_DIRECTORY))
