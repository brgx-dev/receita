import zipfile

def unzip_data(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("unzipped_csv_files")
    print("Unzipped {} to unzipped_csv_files/".format(zip_file_path))
