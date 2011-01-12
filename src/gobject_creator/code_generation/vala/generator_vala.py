#coding=UTF-8

from metamodel.meta_objects import *

from code_generation import Target, get_template_path
from code_generation.generation_inout import *

from code_generation.scope import Scope
from code_generation.parser import Parser

import os.path

class Generator(object):
    
    _DIR = os.path.dirname(__file__)
    
    def __init__(self):
        
        UserCode.setCommentStyle(UserCode.COMMENT_CPP)
    
    def createPackage(self, inPackage, 
        inInput = GenInputNull(),
        inOutput = GenOutputStd()
        ):
        
        for pack in list(inPackage.subPacks.values()):
            self.createPackage(pack, inInput, inOutput)
            
        for cls in list(inPackage.classes.values()):
            self.createClass(cls, inInput, inOutput)
            
        for intf in list(inPackage.intfs.values()):
            self.createInterface(intf, inInput, inOutput)

    def createClass(self, 
                    inClass, 
                    inInput = GenInputNull(),
                    inOutput = GenOutputStd()
                    ):
        
        fileName = inClass.name + ".vala"
        
        self._writeCode(fileName, inClass, self._createClassCode, 
                        inInput, inOutput)
        
    def createInterface(self, 
                        inIntf, 
                        inInput = GenInputNull(),
                        inOutput = GenOutputStd()
                        ):
        
        fileName = inIntf.name + ".vala"
        
        self._writeCode(fileName, inIntf, self._createIntfCode, 
                        inInput, inOutput)
    
    def _createClassCode(self,
                         inClass,
                         inUserCode
                         ):
        
        scope = Scope()
        scope.set_user_code(inUserCode)
        scope.addSymbol("class", inClass)
        scope.addSymbol("absName", self._absName)
        scope.addSymbol("argList", self._argList)
        scope.addSymbol("hasSuperClass", self._hasSuperClass)
        scope.addSymbol("intfList", self._intfList)
        scope.addSymbol("overwritten", self._overwrittenMethods(inClass))
        scope.addSymbol("propertyType", self._propertyType)
                        
        return Parser(scope).parseFile(self._templatePath("class.tmpl"))
    
    def _createIntfCode(self,
                        inIntf,
                        inUserCode 
                        ):
    
        scope = Scope()
        scope.set_user_code(inUserCode)
        scope.addSymbol("interface", inIntf)
        scope.addSymbol("absName", self._absName)
        scope.addSymbol("argList", self._argList)
                        
        return Parser(scope).parseFile(self._templatePath("intf.tmpl"))
        
    def _absName(self, inScope, inClassSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        
        return self._fullName(cls)
    
    def _argList(self, inScope, inMethodSymbol):
        
        result = ""
        
        meth = inScope.getSymbol(inMethodSymbol)
        for param in meth.params:
            if result:
                result += ", "
            result += "%s %s" % (param.type_, param.name)
        
        return result
    
    def _fullName(self, inClif):
        
        result = inClif.name
        package = inClif.package
        while package:
            result = package.name + "." + result
            package = package.package
        
        return result
    
    def _hasSuperClass(self, inScope, inClassSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        
        return bool(cls.superClass)
    
    def _intfList(self, inScope, inClassSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        
        result = ""
        for intf in cls.intfImpls:
            if result:
                result += ", "
            result += self._fullName(intf)
            
        return result

    def _overwrittenMethods(self, inClass):
        
        return [item[0] for item in inClass.overwritten]
    
    def _propertyType(self, inScope, inPropName):
        
        prop = inScope.getSymbol(inPropName)
    
        typeNames = { 
            PROP_BOOLEAN : "bool",
            PROP_INT : "int",
            PROP_DOUBLE : "double",
            PROP_STRING : "string",
            PROP_OBJECT : prop.gobjectType
            }
        
        return typeNames[prop.type_]
    
    def _writeCode(self, 
                   inName, 
                   inClif, 
                   inCreatorMethod, 
                   inInput, 
                   inOutput
                   ):
        
        userCode = inInput.getUserCode(inName)
        codeLines = inCreatorMethod(inClif, userCode)
        
        inOutput.open(inName)
        inOutput.writeCode(codeLines)
        inOutput.close()
        
    def _templatePath(self, inTemplName):
        
        return get_template_path(Target.VALA, inTemplName)
