import os
import subprocess

def run_preparation():
    # Create the upload_files directory if it doesn't exist
    upload_dir = '../upload_files'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Execute the convert_to_utf8.sh script
    subprocess.run(['bash', 'scripts/convert_to_utf8.sh'], check=True)

# Main execution block
if __name__ == "__main__":
    run_preparation()
