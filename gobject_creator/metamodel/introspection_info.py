# coding=UTF-8

from metamodel.meta_objects import Result, Class

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
        