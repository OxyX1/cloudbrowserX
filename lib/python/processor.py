import os
from lib.python.lib.builder import builder
import time

def startup():
    print("converting cpp files...")
    converter = builder()
    converter.builder.convert('lib/cpp/gui.cpp', 'lib/cpp/build/dll/')
    print("converted.")
    time.sleep(1)
    print("running path")
    os.system('python lib/python/gui.py')


startup()