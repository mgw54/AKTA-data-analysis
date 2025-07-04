import subprocess
import sys
import os

requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])