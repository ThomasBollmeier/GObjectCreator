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

import os

def codesnippet_package(line_begin):
    
    block = Textblock(line_begin)
    block.append('with Package("<package_name>"):')
    block.indent()
    block.append()
    block.append("pass # Add objects...")
    
    return str(block)

def codesnippet_class(line_begin):
    
    block = Textblock(line_begin)
    block.append('with Class("<class_name>"):')
    block.indent()
    block.append()
    block.append("pass # Add members...")
    
    return str(block)

def codesnippet_interface(line_begin):
    
    block = Textblock(line_begin)
    block.append('with Interface("<interface_name>"):')
    block.indent()
    block.append()
    block.append("pass # Add members...")
    
    return str(block)

def codesnippet_implements(line_begin):
    
    block = Textblock(line_begin)
    block.append("Implements(<interface>)")
    
    return str(block)

def codesnippet_constructor(line_begin):
    
    block = Textblock(line_begin)
    block.append("with Constructor():")
    block.indent()
    block.append('ConstructorParam("<name>", "<type>")')
    
    return str(block)

def codesnippet_constructor_param(line_begin):
    
    block = Textblock(line_begin)
    block.append('ConstructorParam("<name>", "<type>")')
    
    return str(block)

def codesnippet_init_property(line_begin):
    
    block = Textblock(line_begin)
    block.append('InitProperty("<name>", "<value>")')
    
    return str(block)

def codesnippet_attr(line_begin):
    
    block = Textblock(line_begin)
    block.append(
        'Attr("<name>", "<type>")'
    )
        
    return str(block)

def codesnippet_property(line_begin):
    
    block = Textblock(line_begin)
    block.append('Property(')
    block.indent()
    block.append('"<name>",')
    block.append('"<description>",')
    block.append('inType = PROP_STRING,')
    block.append('inAccess = PROP_ACCESS_READ, \
    #PROP_ACCESS_CONSTRUCTOR, PROP_READ_WRITE')
    block.append(')')
    
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