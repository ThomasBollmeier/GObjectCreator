#coding=UTF-8

import re
import os

class PreProcessor(object):
    
    _INCLUDE_REGEX = re.compile(r'\s*#include_def\s+<(.*)>\Z')
    
    def __init__(self):
        
        self._search_paths = [os.curdir]
        
    def add_paths(self, in_paths):
        
        for path in in_paths:
            if path not in self._search_paths:
                self._search_paths.append(path)

    def scan_for_includes(self, in_def_file):
    
        result = []
        search_paths = self._search_paths
        if os.path.dirname(in_def_file) not in search_paths:
            search_paths.insert(0, os.path.dirname(in_def_file))
    
        f = open(in_def_file, "r")
        lines = f.readlines()
        f.close()
    
        for line in lines:
            line = line.strip()
            match_obj = PreProcessor._INCLUDE_REGEX.match(line)
            if match_obj:
                result.append(self.full_name(match_obj.group(1), search_paths))
            
        return result
    
    def full_name(self, in_base_name, in_search_paths=[]):
        
        if in_search_paths:
            search_paths = in_search_paths
        else:
            search_paths = self._search_paths
        
        for path in search_paths:
            full_name = path + os.sep + in_base_name
            if os.path.exists(full_name):
                return full_name
    
        raise FileNotFound(in_base_name)

class FileNotFound(Exception): 
    
    def __init__(self, in_name):
        
        Exception.__init__(self)
        
        self._name = in_name
        
    def __str__(self):
        
        return "File %s could not be found!" % self._name
