import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to get WORKDIR from environment variable
WORKDIR = os.getenv("WORKDIR")

# If WORKDIR is not set or doesn't exist, use the current directory
if not WORKDIR or not os.path.exists(WORKDIR):
    WORKDIR = os.getcwd()

print(f"Current WORKDIR: {WORKDIR}")
print(f"Contents of WORKDIR: {os.listdir(WORKDIR)}")

# Ensure the src directory is in the Python path
src_dir = os.path.join(WORKDIR, 'src')
if src_dir not in os.sys.path:
    os.sys.path.append(src_dir)

def get_workdir():
    return WORKDIR