# coding=UTF-8

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

from .meta_objects import Result, Class

class ParamCategory:
    
    IN = 1
    OUT = 2
    INOUT = 3
    USER_DATA = 4
    RESULT = 5
         
class TransferMode:
    
    NONE = 1
    CONTAINER_ONLY = 2
    FULL = 3
    UNSPECIFIED = 4
    
class DataType:
    
    POINTER = "any"
    BOOLEAN = "boolean"
    INTEGER = "int"
    SIZE_T = "size_t"
    GTYPE = "GType"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "utf8"
    FILENAME = "filename"
    GOBJECT = "Object"
    UNSPECIFIED = ""

class IntrospectionInfo(object):
    
    def __init__(self, in_param = None):
        
        if in_param is None or not isinstance(in_param, Result):
            self.category = ParamCategory.IN
            self.transfer_mode = TransferMode.UNSPECIFIED
        else:
            self.category = ParamCategory.RESULT
            clif = in_param.method.clif
            if isinstance(clif, Class) and in_param.method == clif.constructor:
                self.transfer_mode = TransferMode.FULL
            else:
                self.transfer_mode = TransferMode.UNSPECIFIED
        self.data_type = DataType.UNSPECIFIED
        self.description = ""
        
        # relevant für Arrays:
        self.is_array = False
        self.fixed_length = 0
        self.length_from_param = ""
        self.null_terminated = False
        self.element_type = DataType.UNSPECIFIED
        
        # relevant für Hashtabellen:
        self.is_dictionary = False
        self.key_type = DataType.UNSPECIFIED
        self.value_type = DataType.UNSPECIFIED 
        
