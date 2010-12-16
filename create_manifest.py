#!/usr/bin/python

import os

def get_files(dirpath="", recursive=True):
    
    result = []
 
    if not dirpath:
        dir = "."
    else:
        dir = dirpath
        
    paths = os.listdir(dir)
    paths.sort()
    
    for path in paths:
        if dirpath:
            path = dirpath + os.sep + path
        if os.path.isfile(path):   
            result.append(path)
        elif os.path.isdir(path) and recursive:
            for file in get_files(path, recursive):
                result.append(file)
                
    return result
                
all_files = get_files(recursive=False)
all_files += get_files(dirpath="bin")
all_files += get_files(dirpath="examples")
all_files += get_files(dirpath="gobject_creator")

for file in all_files:
    print file