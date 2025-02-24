import os
import platform
import subprocess

def install_dependencies():
    os_type = platform.system()
    if os_type == "Darwin":
        subprocess.run(["brew", "install", "postgresql"])
    elif os_type == "Linux":
        subprocess.run(["sudo", "apt", "install", "postgresql"])
    else:
        print("Unsupported OS. Please install PostgreSQL manually.")
