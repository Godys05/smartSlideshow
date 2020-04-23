import os
from time import sleep

def getImages(path):
    for root, directories, f in os.walk(path):
        for file in f:
            if ('.jpg' in file or '.png' in file or '.jpeg' in file):
                files.append(os.path.join(root, file))
        return files

files = []
