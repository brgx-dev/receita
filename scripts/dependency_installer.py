import os
import platform
import subprocess

def install_dependencies():
    os_type = platform.system()
    if os_type == "Darwin":  # macOS
        subprocess.run(["brew", "install", "postgresql"])
        subprocess.run(["pip3", "install", "requests"])  # Install requests
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "postgresql"])
        subprocess.run(["pip3", "install", "requests"])  # Install requests
    else:
        print("Unsupported OS. Please install PostgreSQL and requests manually.")
