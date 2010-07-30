#coding=UTF-8

import re
import os
import subprocess

class MarshallerGenerator(object):
    
    def __init__(self, inClass):
        
        self._signals = [method for method in inClass.methods if method.isSignal]
        self._prefix = inClass.prefix()
                
        self._initTypeRegexs()
        
    def getCode(self, inHeader=True):
        
        result = []
        
        lines = self._getListCode()
        if not lines:
            return result
        
        input_name = "input%s" % os.getpid()
        input_file = open(input_name, "w")
        for line in lines:
            input_file.write(line + "\n")
        input_file.close()
            
        output_name = "output%s" % os.getpid()
        output_file = open(output_name, "w")
        
        if inHeader:
            cmd = "cat %s | glib-genmarshal --prefix=%s --header" % (input_name, self._prefix)
        else:
            cmd = "cat %s | glib-genmarshal --prefix=%s --body" % (input_name, self._prefix)
            
        subprocess.call(cmd, shell=True, stdout=output_file)
        
        output_file.close()
        
        output_file = open(output_name, "r")
        
        result = [line.strip() for line in output_file.readlines()]
        
        output_file.close()
        
        os.remove(input_name)
        os.remove(output_name)
        
        return result
    
    def getMarshallerName(self, inSignalMethod):
        
        result = self._prefix
        
        result += "_" + self._getType(inSignalMethod.resultType) + "_"
        
        if inSignalMethod.params:
            for param in inSignalMethod.params:
                result += "_" + self._getType(param.type_)
        else:
            result = "VOID"
        
        return result
    
    def getArgsGTypes(self, inSignalMethod):
        
        result = []
        
        for param in inSignalMethod.params:
            result.append(self._getGType(param.type_))
                
        return result
    
    def getResultGType(self, inSignalMethod):
        
        return self._getGType(inSignalMethod.resultType)
            
    def _getListCode(self):
        
        result = []
        
        for signal in self._signals:
            line = self._getType(signal.resultType) + ": "
            if signal.params:
                paramStr = ""
                for param in signal.params:
                    if paramStr:
                        paramStr += ", "
                    paramStr += self._getType(param.type_)
            else:
                paramStr = "VOID"
            line += paramStr
            result.append(line)
            
        return result
                
    def _getType(self, inParameterType):
        
        paramType = inParameterType.strip()
        
        for regex, typeStr, gTypeStr in self._regexs:
            if regex.match(paramType):
                return typeStr
            
        return "OBJECT"
    
    def _getGType(self, inParameterType):
        
        paramType = inParameterType.strip()
        
        for regex, typeStr, gTypeStr in self._regexs:
            if regex.match(paramType):
                return gTypeStr
            
        return "G_TYPE_OBJECT"
    
    def _initTypeRegexs(self):
        
        self._regexs = []
        
        self._regexs.append((re.compile(r".*void"), "VOID", "G_TYPE_NONE"))
        self._regexs.append((re.compile(r".*gboolean"), "BOOLEAN", "G_TYPE_BOOLEAN"))
        self._regexs.append((re.compile(r".*gint"), "INT", "G_TYPE_INT"))
        self._regexs.append((re.compile(r".*gfloat"), "FLOAT", "G_TYPE_FLOAT"))
        self._regexs.append((re.compile(r".*gdouble"), "DOUBLE", "G_TYPE_DOUBLE"))
        self._regexs.append((re.compile(r".*gchar*"), "STRING", "G_TYPE_STRING"))

    