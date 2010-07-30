# coding=UTF-8

from classmate.metamodel.introspection_info import ParamCategory, \
    IntrospectionInfo, DataType, TransferMode

# Parametertypen:
    
def Input(in_param):
    return _category(in_param, ParamCategory.IN)

def Output(in_param):
    return _category(in_param, ParamCategory.OUT)

def InOutput(in_param):
    return _category(in_param, ParamCategory.INOUT)

def UserData(in_param):
    return _category(in_param, ParamCategory.USER_DATA)

# Beschreibung:

class Description(object):
    
    def __init__(self, inDescription):
        
        self._descr = inDescription
        
    def __call__(self, in_param):
        
        res = _decorate(in_param)
        res.introspection.description = self._descr
        
        return res

# Übergabemodus bzgl. Eigentümerschaft für allokatierten Speicher:

class Transfer(object):
    
    def __init__(self, inMode):
        
        self._mode = inMode
        
    def __call__(self, in_param):
        
        res = _decorate(in_param)
        res.introspection.transfer_mode = self._mode
        
        return res
    
class TransNone(Transfer):
    
    def __init__(self):
        
        Transfer.__init__(self, TransferMode.NONE)
        
class TransFull(Transfer):
    
    def __init__(self):
        
        Transfer.__init__(self, TransferMode.FULL)
        
class TransContainer(Transfer):
    
    def __init__(self):
        
        Transfer.__init__(self, TransferMode.FULL)
            
# Datentyp:

class IntroSpectionType(object):
    
    def __init__(self, inDataType):
        
        self._dtype = inDataType
        
    def __call__(self, in_param):
        
        res = _decorate(in_param)
        res.introspection.data_type = self._dtype
        
        return res
    
# Arrays:

class Array(object):
    
    def __init__(self,
                 inFixedLength = 0,
                 inLengthFromParam = "",
                 inNullTerminated = False,
                 inElementType = DataType.UNSPECIFIED
                 ):
    
        self._len = inFixedLength
        self._pname = inLengthFromParam
        self._null_terminated = inNullTerminated
        self._elem_type = inElementType
        
    def __call__(self, in_param):
        
        res = _decorate(in_param)
        
        res.introspection.is_array = True
        res.introspection.fixed_length = self._len
        res.introspection.length_from_param = self._pname
        res.introspection.null_terminated = self._null_terminated
        res.introspection.element_type = self._elem_type
        
        return res
    
# Hashes:

class HashTable(object):
    
    def __init__(self, inKeyType, inValueType):
        
        self._key = inKeyType
        self._val = inValueType
        
    def __call__(self, in_param):
        
        res = _decorate(in_param)
        
        res.introspection.is_dictionary = True
        res.introspection.key_type = self._key
        res.introspection.value_type = self._val
        
        return res 
    
# Hilfsfunktionen:

def _category(in_param, in_category):
    
    res = _decorate(in_param)
    res.introspection.category = in_category
    
    return res
         
def _decorate(in_param):
    
    if not hasattr(in_param, "introspection"):
        in_param.introspection = IntrospectionInfo(in_param)
        
    return in_param

