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

from class_dialog import run_class_dialog
from interface_dialog import InterfaceDialog
from method_dialog import run_method_dialog
from property_dialog import PropertyDialog
from metamodel.meta_objects import *

def codesnippet_package(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('with Package("<package_name>"):')
    block.indent()
    block.writeln()
    block.writeln("pass # Add objects...")
    
    return str(block)

def codesnippet_class(line_begin):
    
    result = run_class_dialog()
    if not result:
        return
    
    name, super_class, abstract, prefix = result
            
    block = Textblock(line_begin)
    indented = False
    
    if not super_class and not abstract and not prefix:
        block.writeln('with Class("%s"):' % name)
    else:
        block.write('with Class("%s"' % name)
        if super_class:
            block.writeln(",")
            block.indent()
            indented = True
            block.write("inSuperClass = %s" % super_class)
        if prefix:
            block.writeln(",")
            if not indented:
                block.indent()
                indented = True
            block.write('inAlias = "%s"' % prefix)
        if abstract:
            block.writeln(",")
            if not indented:
                block.indent()
                indented = True
            block.write('inAbstract = %s' % abstract)
        block.writeln()
        block.writeln("):")
    
    if not indented:
        block.indent()
    block.writeln()
    block.writeln("pass # Add members...")
    
    return str(block)

def codesnippet_interface(line_begin):
    
    data = InterfaceDialog().run()
    if not data:
        return
    
    name, prefix = data

    block = Textblock(line_begin)
    if not prefix:
        block.writeln('with Interface("%s"):' % name)
        block.indent()
    else:
        block.writeln('with Interface("%s",' % name)
        block.indent()
        block.writeln('inAlias = "%s"' % prefix)
        block.writeln("):")
    
    block.writeln()
    block.writeln("pass # Add members...")
    
    return str(block)

def codesnippet_implements(line_begin):
    
    block = Textblock(line_begin)
    block.writeln("Implements(<interface>)")
    
    return str(block)

def codesnippet_constructor(line_begin):
    
    block = Textblock(line_begin)
    block.writeln("with Constructor():")
    block.indent()
    block.writeln('ConstructorParam("<name>", "<type>")')
    
    return str(block)

def codesnippet_constructor_param(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('ConstructorParam("<name>", "<type>")')
    
    return str(block)

def codesnippet_init_property(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('InitProperty("<name>", "<value>")')
    
    return str(block)

def codesnippet_method(line_begin):
    
    res = run_method_dialog(is_intf_method = False)
    if not res:
        return
    
    name, visibility, scope, virtual, abstract = res
    
    block = Textblock(line_begin)
    block.writeln('with Method("%s",' % name)
    block.indent()
    visi_names = { PUBLIC: "PUBLIC", 
                   PROTECTED: "PROTECTED",
                   PRIVATE: "PRIVATE"
                   }
    block.write("inVisi = %s" % visi_names[visibility])
    if scope == STATIC:
        block.writeln(",")
        block.write("inScope = STATIC")
    if abstract:
        block.writeln(",")
        block.write("inAbstract = True")
    elif virtual:
        block.writeln(",")
        block.write("inVirtual = True")
    block.writeln()
    block.writeln("):")
    block.writeln()
    block.writeln('Param("<name>", "<type>")')
        
    return str(block)

def codesnippet_result(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('Result("<type>")')
        
    return str(block)

def codesnippet_param(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('Param("<name>", "<type>")')
        
    return str(block)

def codesnippet_override(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('Override("<method_name>")')
        
    return str(block)

def codesnippet_attr(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('Attr("<name>", "<type>")')
        
    return str(block)

def codesnippet_property(line_begin):
    
    prop_attrs = PropertyDialog().run()
    if not prop_attrs:
        return
    
    name, description, property_type, \
        gobject_type, access_type = prop_attrs
    
    if not description:
        description = name
        
    prop_type = {}
    prop_type[PROP_BOOLEAN] = "PROP_BOOLEAN"
    prop_type[PROP_INT] = "PROP_INT"
    prop_type[PROP_DOUBLE] = "PROP_DOUBLE"
    prop_type[PROP_STRING] = "PROP_STRING"
    prop_type[PROP_POINTER] = "PROP_POINTER"
    prop_type[PROP_OBJECT] = "PROP_OBJECT"
    prop_type[PROP_ENUM] = "PROP_ENUM"
    
    access = {}
    access[PROP_ACCESS_READ] = "PROP_ACCESS_READ"
    access[PROP_ACCESS_CONSTRUCTOR] = "PROP_ACCESS_CONSTRUCTOR"
    access[PROP_ACCESS_READ_WRITE] = "PROP_ACCESS_READ_WRITE"
    
    block = Textblock(line_begin)
    block.writeln('Property(')
    block.indent()
    block.writeln('"%s",' % name)
    block.writeln('"%s",' % description)
    block.writeln('inType = %s,' % prop_type[property_type])
    if gobject_type:
        block.writeln('inGObjectType = "%s",' % gobject_type)
    block.writeln('inAccess = %s,' % access[access_type])
    block.writeln("inMin = None,")
    block.writeln("inMax = None,")
    block.writeln("inDefault = None")
    block.writeln(')')
    
    return str(block)

def codesnippet_signal(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('with Signal("<signal-name>"):')
    block.indent()
    block.writeln('Param("<name>", "<type>")')
        
    return str(block)

def codesnippet_extends(line_begin):
    
    block = Textblock(line_begin)
    block.writeln('Extends(<interface>)')
    
    return str(block)
    
def codesnippet_intf_method(line_begin):
    
    res = run_method_dialog(is_intf_method = True)
    if not res:
        return
    
    name, visibility, scope, virtual, abstract = res
    
    block = Textblock(line_begin)
    block.writeln('with IntfMethod("%s"):' % name)
    block.indent()
    block.writeln('Param("<name>", "<type>")')
        
    return str(block)

class Textblock(object):
    
    def __init__(self, line_begin):
        
        self._line_begin = line_begin
        self._num_tabs = 0
        self._lines = []
        self._current_line = ""
        
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
        
    def write(self, text):
        
        self._current_line += text
        
    def writeln(self, line=""):
        
        if self._current_line:
            line = self._current_line + line
            self._current_line = ""
        
        if self._lines:
            line = self._line_begin + "\t" * self._num_tabs + line
        self._lines.append(line)
