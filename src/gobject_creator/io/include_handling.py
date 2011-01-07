#coding=UTF-8

"""
This file is part of GObjectCreator.

GObjectCreator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GObjectCreator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GObjectCreator (see file COPYING). If not, see
<http://www.gnu.org/licenses/>.
"""

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
                
    @staticmethod
    def get_include_names(in_def_file):
     
        result = []
        
        f = open(in_def_file, "r")
        lines = f.readlines()
        f.close()
        
        for line in lines:
            line = line.strip()
            match_obj = PreProcessor._INCLUDE_REGEX.match(line)
            if match_obj:
                result.append(match_obj.group(1))
                
        return result

    def scan_for_includes(self, in_def_file):
    
        result = []
        search_paths = self._search_paths
        
        if os.path.dirname(in_def_file) not in search_paths:
            search_paths.insert(0, os.path.dirname(in_def_file))
    
        for include_name in PreProcessor.get_include_names(in_def_file):
            result.append(self.full_name(include_name, search_paths))
            
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
