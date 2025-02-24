import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_extraction(zip_file_path):
    logging.info("Unzipped {} to {}".format(zip_file_path, EXTRACTION_DIRECTORY))
