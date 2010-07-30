# coding=UTF-8

from classmate.metamodel.meta_objects import INSTANCE
from classmate.metamodel.introspection_info import ParamCategory, TransferMode, DataType, \
    IntrospectionInfo
    
import re

def create_annotation(in_prefix, in_method):
    """
    Annotation für GObject-Introspection erzeugen:
    """
        
    result = ""
    
    lines = []
    lines.append("/**")
    
    line = "* %s_%s:" % (in_prefix, in_method.name)
    lines.append(line)
    lines.append("*")
    
    params = [_ParamInfo.create(p) for p in in_method.params]
    
    if in_method.scope == INSTANCE:
        info = IntrospectionInfo()
        info.category = ParamCategory.IN
        info.transfer_mode = TransferMode.NONE
        params.insert(0, _ParamInfo("self", info))
        
    if params:
        for param in params:
            line = "* @%s:" % param.name
            hlp = param.info_string()
            if hlp:
                line += " %s:" % hlp
            hlp = param.description()
            if hlp:
                line += " " + hlp
            lines.append(line)
        lines.append("*")
    
    if in_method.resultType != "void":
        line = "* Return value:"
        result_param = _ParamInfo.create(in_method.result)
        hlp = result_param.info_string()
        if hlp:
            line += " %s:" % hlp
        hlp = result_param.description()
        if hlp:
            line += " " + hlp
        lines.append(line)
        lines.append("*")
    
    lines.append("*/")
    
    for line in lines:
        if result:
            result += "\n"
        result += line
        
    return result

class _ParamInfo(object):
    
    @staticmethod
    def create(in_param):
        
        try:
            info = in_param.introspection
        except AttributeError:
            info = _ParamInfo._create_default_info(in_param)
                                 
        return _ParamInfo(in_param.name, info)
    
    def __init__(self,
                 in_name,
                 in_info
                 ):

        self.name = in_name        
        self.info = in_info
        
    def info_string(self):
        
        res = ""
        
        hlp = ""
        
        if self.info.category == ParamCategory.IN:
            hlp = "(in)"
        elif self.info.category == ParamCategory.OUT:
            hlp = "(out)"
        elif self.info.category == ParamCategory.INOUT:
            hlp = "(inout)"
        elif self.info.category == ParamCategory.USER_DATA:
            hlp = "(closure)"
        res = self._add_info(hlp, res)
            
        hlp = ""
        
        if self.info.transfer_mode == TransferMode.NONE:
            hlp = "(none)"
        elif self.info.transfer_mode == TransferMode.CONTAINER_ONLY:
            hlp = "(container)"
        elif self.info.transfer_mode == TransferMode.FULL:
            hlp = "(full)"
        res = self._add_info(hlp, res)
        
        if self.info.data_type != DataType.UNSPECIFIED:
            res = self._add_info("(type %s)" % self.info.data_type, res)
            
        hlp = ""
        
        if self.info.is_array:
            
            hlp = "(array"
            
            if self.info.fixed_length:
                hlp += " fixed-size=%d" % self.info.fixed_length
            elif self.info.length_from_param:
                hlp += " length=%s" % self.info.length_from_param
            
            if self.info.null_terminated:
                hlp += " zero-terminated=1"
            
            hlp += ")"
            
            if self.info.element_type != DataType.UNSPECIFIED:
                hlp += " (element-type %s)" % self.info.element_type
                        
        elif self.info.is_dictionary:
            
            if self.info.key_type != DataType.UNSPECIFIED and \
               self.info.value_type != DataType.UNSPECIFIED:
                
                hlp = "(element-type %s %s)" % (self.info.key_type, self.info.value_type)
        
        res = self._add_info(hlp, res)
                    
        return res
    
    def description(self):
        
        return self.info.description
    
    def _add_info(self, in_info_str, in_total_info):
        
        res = in_total_info
        
        if not in_info_str:
            return res
        
        if res:
            res += " "
        res += in_info_str
        
        return res
    
    # Namenskonventionen für Parameter:
    _REGEX_IN_PARAM = re.compile(r"\Ain_.*")
    _REGEX_OUT_PARAM = re.compile(r"\Aout_.*")
    _REGEX_INOUT_PARAM = re.compile(r"\Ainout_.*")
    
    @staticmethod
    def _create_default_info(in_param):
        
        result = IntrospectionInfo(in_param)
        
        if _ParamInfo._REGEX_IN_PARAM.match(in_param.name):
            result.category = ParamCategory.IN
        elif _ParamInfo._REGEX_OUT_PARAM.match(in_param.name):
            result.category = ParamCategory.OUT
        elif _ParamInfo._REGEX_INOUT_PARAM.match(in_param.name):
            result.category = ParamCategory.INOUT
            
        return result        