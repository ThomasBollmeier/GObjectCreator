# coding=UTF-8

from metamodel.meta_objects import *
from code_generation.generation_inout import *

from code_generation.scope import Scope
from code_generation.parser import Parser

import os.path

_DIR = os.path.dirname(__file__)
            
class Generator(object):

    def __init__(self):
        
        UserCode.setCommentStyle(UserCode.COMMENT_CPP)
                
    def createPackage(self, inPackage, 
        inInput = GenInputNull(),
        inOutput = GenOutputStd()
        ):
        
        for pack in inPackage.subPacks.values():
            self.createPackage(pack, inInput, inOutput)
            
        for cls in inPackage.classes.values():
            self.createClass(cls, inInput, inOutput)
            
        for intf in inPackage.intfs.values():
            self.createInterface(intf, inInput, inOutput)

    def createClass(self, 
                    inClass, 
                    inInput = GenInputNull(),
                    inOutput = GenOutputStd()
                    ):
        
        name = "%s.cs" % inClass.name
        self._writeCode(name, inClass, self._createClassCode,
                        inInput, inOutput)
        
    def createInterface(self, 
                        inIntf, 
                        inInput = GenInputNull(),
                        inOutput = GenOutputStd()
                        ):
        
        name = "%s.cs" % inIntf.name
        self._writeCode(name, inIntf, self._createIntfCode,
                        inInput, inOutput)
    
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
   
    def _createClassCode(self,
                         inClass,
                         inUserCode
                         ):
        
        scope = Scope()
        self._initClassScope(scope, inClass)
        scope.set_user_code(inUserCode)
                
        parser = Parser(scope)
        
        return parser.parseFile(self._templatePath("class.tmpl"))

    def _createIntfCode(self,
                        inIntf,
                        inUserCode
                        ):
        
        scope = Scope()
        self._initIntfScope(scope, inIntf)
        scope.set_user_code(inUserCode)
                
        parser = Parser(scope)
        
        return parser.parseFile(self._templatePath("intf.tmpl"))

    def _initClassScope(self, inScope, inClass):
        
        self._initClifScope(inScope, inClass)
        
        inScope.addSymbol("class", inClass)
        inScope.addSymbol("hasSuper", bool(inClass.superClass))
        inScope.addSymbol("overwritten", self._overwrittenMethods(inClass))
        inScope.addSymbol("classDecl", self._classDecl)

    def _initIntfScope(self, inScope, inIntf):
        
        self._initClifScope(inScope, inIntf)
        
        inScope.addSymbol("intf", inIntf)
    
    def _initClifScope(self, inScope, inClif):
        
        inScope.addSymbol("Name", inClif.name)
        inScope.addSymbol("sig", self._signature)
        inScope.addSymbol("methBegin", self._methodBeginDecl)
        inScope.addSymbol("nspace", self._nspace)
           
    def _absName(self, inClif):
        
        result = inClif.name
        ns = self._namespace(inClif)
        if ns:
            result = ns + "." + result
            
        return result
             
    def _classDecl(self, inScope, inClassSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        
        if not cls.abstract:
            result = "public class %s" % cls.name
        else:
            result = "public abstract class %s" % cls.name 
        
        clifNames = []
        if cls.superClass:
            clifNames.append(self._absName(cls.superClass))
            
        for intf in cls.intfImpls:
            clifNames.append(self._absName(intf))
            
        if clifNames:
            clifStr = ""
            for clifName in clifNames:
                if clifStr:
                    clifStr += ", "
                clifStr += clifName
                
            result += " : " + clifStr
        
        return result
    
    def _methodBeginDecl(self, inScope, inMethodSymbol):
        
        meth = inScope.getSymbol(inMethodSymbol)
        
        if meth.visi == PUBLIC:
            result = "public"
        elif meth.visi == PROTECTED:
            result = "protected"
        elif meth.visi == PRIVATE:
            result = "private"
            
        if meth.scope == STATIC:
            result += " static"
        
        if meth.virtual:
            result += " virtual"
                
        result += " " + meth.resultType
        
        return result
    
    def _namespace(self, inClif):
        
        result = ""
        
        pack = inClif.package
        while pack:
            if result:
                result = pack.name + "." + result
            else:
                result = pack.name
            pack = pack.package
            
        return result
    
    def _nspace(self, inScope, inClassSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        
        return self._namespace(cls)
    
    def _overwrittenMethods(self, inClass):
        
        return [meth for meth, intf in inClass.overwritten
                if intf is None]   
    
    def _signature(self, inScope, inMethodSymbol):
        
        result = ""
        
        meth = inScope.getSymbol(inMethodSymbol)
        
        for param in meth.params:
            if result:
                result += ", "
            result += "%s %s" % (param.type_, param.name)
            
        return result
    
    def _templatePath(self, inTemplName):
        
        return _DIR + os.sep + "templates" + os.sep + inTemplName
        
