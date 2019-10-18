import os
import sys

def __prepare_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_paths(paths):
    if isinstance(paths,str):
        __prepare_path(paths)
    if isinstance(paths,list):
        for path in paths:
            __prepare_path(path)
    
