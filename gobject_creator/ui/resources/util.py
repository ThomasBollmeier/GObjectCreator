import os

def get_resource_path(file_name):
    
    path = os.path.dirname(__file__)
    path = os.path.abspath(path)
    
    return path + os.sep + file_name
    