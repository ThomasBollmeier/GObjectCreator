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
<http://www.gnu.
"""

import os

def codesnippet_package(line_begin):
    
    block = Textblock(line_begin)
    block.append('with Package("<your_package_name>"):')
    block.indent()
    block.append()
    block.append("pass # Add objects...")
    
    return str(block)

def codesnippet_class(line_begin):
    
    block = Textblock(line_begin)
    block.append('with Class("<your_class_name>"):')
    block.indent()
    block.append()
    block.append("pass # Add members...")
    
    return str(block)

def codesnippet_interface(line_begin):
    
    block = Textblock(line_begin)
    block.append('with Interface("<your_interface_name>"):')
    block.indent()
    block.append()
    block.append("pass # Add methods...")
    
    return str(block)

class Textblock(object):
    
    def __init__(self, line_begin):
        
        self._line_begin = line_begin
        self._num_tabs = 0
        self._lines = []
        
    def __str__(self):
        
        res = ""
        for line in self._lines:
            if res:
                res += os.linesep
            res += line
            
        return res
        
    def indent(self, num_tabs=1):
        
        self._num_tabs += num_tabs
        
    def unindent(self, num_tabs=1):
        
        self._num_tabs -= num_tabs
        
    def append(self, line=""):
        
        if self._lines:
            line = self._line_begin + "\t" * self._num_tabs + line
        self._lines.append(line)