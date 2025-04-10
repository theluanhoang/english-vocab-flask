import os

def cleanup_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)