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

from metamodel.meta_objects import *
from code_generation.generation_inout import *
from code_generation.gobject.gobject_marshaller_generator import MarshallerGenerator
from code_generation.gobject.gobject_introspection_support import create_annotation

from code_generation.scope import Scope
from code_generation.parser import Parser

import os.path

class Generator(object):

    _DIR = os.path.dirname(__file__)

    def __init__(self):

        pass

    def createPackage(self,
        inPackage,
        inInput = GenInputNull(),
        inOutput = GenOutputStd()
        ):

        for pack in inPackage.subPacks.values():
            self.createPackage(pack, inInput, inOutput)

        for cls in inPackage.classes.values():
            self.createClass(cls, inInput, inOutput)

        for intf in inPackage.intfs.values():
            self.createInterface(intf, inInput, inOutput)
            
        for errorDomain in inPackage.errorDomains.values():
            self.createErrorDomain(errorDomain, inInput, inOutput)
            
        for enum in inPackage.enums.values():
            self.createEnumeration(enum, inOutput)
            
    def createClass(self,
                    inClass,
                    inInput = GenInputNull(),
                    inOutput = GenOutputStd()
                    ):

        fileName = self._filename(None, inClass) + ".h"

        self._writeCode(fileName, inClass, self._createClassHeaderCode,
                        inInput, inOutput)

        fileName = self._filename(None, inClass) + ".c"

        self._writeCode(fileName, inClass, self._createClassImplCode,
                        inInput, inOutput)
        
        if self._hasProtectedAttrs(inClass) or self._hasProtectedMethods(inClass):
            
            fileName = self._filename(None, inClass) + "_prot.h"

            self._writeCode(fileName, inClass, self._createClassProtectedHeaderCode,
                            inInput, inOutput)
        
        self._createMarshallers(inClass, inOutput)

    def createInterface(self,
                        inIntf,
                        inInput = GenInputNull(),
                        inOutput = GenOutputStd()
                        ):

        fileName = self._filename(None, inIntf) + ".h"

        self._writeCode(fileName, inIntf, self._createIntfHeaderCode,
                        inInput, inOutput)

        fileName = self._filename(None, inIntf) + ".c"

        self._writeCode(fileName, inIntf, self._createIntfImplCode,
                        inInput, inOutput) 
        
    def createErrorDomain(self, inErrorDomain, inInput, inOutput):
        
        fileName = self._filename(None, inErrorDomain) + ".h"

        self._writeCode(fileName, inErrorDomain, self._createErrorDomainHeaderCode,
                        inInput, inOutput)

        fileName = self._filename(None, inErrorDomain) + ".c"

        self._writeCode(fileName, inErrorDomain, self._createErrorDomainSourceCode,
                        inInput, inOutput) 
        
    def createEnumeration(self, inEnum, inOutput):
        
        
        
        scope = Scope()
        self._initEnumerationScope(scope, inEnum)
        
        if not inEnum.isFlagType:
            
            fileName = self._filename(None, inEnum) + ".h"
                    
            codeLines = Parser(scope).parseFile(self._templatePath("enum_class_header.tmpl"))
            
            inOutput.open(fileName)
            inOutput.writeCode(codeLines)
            inOutput.close()

            fileName = self._filename(None, inEnum) + ".c"
                    
            codeLines = Parser(scope).parseFile(self._templatePath("enum_class_source.tmpl"))
            
            inOutput.open(fileName)
            inOutput.writeCode(codeLines)
            inOutput.close()
        
        else:
            
            fileName = self._filename(None, inEnum) + ".h"
                    
            codeLines = Parser(scope).parseFile(self._templatePath("flags.tmpl"))
            
            inOutput.open(fileName)
            inOutput.writeCode(codeLines)
            inOutput.close()
        
    def _allInterfaces(self, inClass):
        
        hlp = {}
        
        for intf in inClass.intfImpls:
            hlp[intf.name] = intf
            hlp.update(intf.getExtendedIntfs(inRecursive=True))
                
        return hlp.values()
                
    def _annotation(self, inScope, inPrefixSymbol, inMethodSymbol):
        
        prefix = inScope.getSymbol(inPrefixSymbol)
        method = inScope.getSymbol(inMethodSymbol)
        
        return create_annotation(prefix, method)
            
    def _camelCaseToUnderScore(self, inName):
        
        result = ""
        lastLow = False
        
        for ch in inName:
            charLow = ch.lower()
            if lastLow and ch != charLow:
                result += "_"
            result += charLow
            lastLow = (ch == charLow)
            
        return result
        
    def _castDefiningClass(self, inScope, inMethod, inClassVarName):

        method = inScope.getSymbol(inMethod)
        cls = method.clif
        namespace = self._packagePrefix(None, cls).upper()
        basename = cls.name.upper()
        if not namespace:
            return "%s_CLASS(%s)" % (basename, inClassVarName)
        else:
            return "%s_%s_CLASS(%s)" % (namespace, basename, inClassVarName)

    def _createClassHeaderCode(self,
        inClass,
        inUserCode
        ):

        scope = Scope()
        self._initClassScope(scope, inClass, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("class_header.tmpl"))
    
    def _createClassProtectedHeaderCode(self,
        inClass,
        inUserCode
        ):

        scope = Scope()
        self._initClassScope(scope, inClass, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("class_header_protected.tmpl"))

    def _createClassImplCode(self,
        inClass,
        inUserCode
        ):

        scope = Scope()
        self._initClassScope(scope, inClass, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("class_source.tmpl"))
    
    def _createIntfHeaderCode(self,
        inIntf,
        inUserCode
        ):

        scope = Scope()
        self._initIntfScope(scope, inIntf, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("intf_header.tmpl"))
    
    def _createIntfImplCode(self,
        inIntf,
        inUserCode
        ):

        scope = Scope()
        self._initIntfScope(scope, inIntf, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("intf_source.tmpl"))   
    
    def _createErrorDomainHeaderCode(self, inErrorDomain, inUserCode):
        
        scope = Scope()
        self._initErrorDomainScope(scope, inErrorDomain, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("error_domain_header.tmpl"))

    def _createErrorDomainSourceCode(self, inErrorDomain, inUserCode):
        
        scope = Scope()
        self._initErrorDomainScope(scope, inErrorDomain, inUserCode)
        
        return Parser(scope).parseFile(self._templatePath("error_domain_source.tmpl"))
    
    def _createMarshallers(self, inClass, inOutput):
        
        mg = MarshallerGenerator(inClass)
        
        lines = mg.getCode(inHeader=True)
        if lines:
            inOutput.open(self._filename(None, inClass) + "_marshaller.h")
            inOutput.writeCode(lines)
            inOutput.close()

        lines = mg.getCode(inHeader=False)
        if lines:
            inOutput.open(self._filename(None, inClass) + "_marshaller.c")
            inOutput.writeCode(lines)
            inOutput.close()

    def _defaultProp(self, inScope, inProperty):

        prop = inScope.getSymbol(inProperty)
        defaults = {
            PROP_BOOLEAN : "FALSE",
            PROP_INT : "0",
            PROP_DOUBLE : "0.0",
            PROP_STRING : '""',
        }

        return self._propValueToString(prop.default, prop.type_, defaults)
    
    def _filename(self, inScope, inClif):
        
        if inScope:
            clif = inScope.getSymbol(inClif)
        else:
            clif = inClif
        
        result = clif.name.lower()
        package = clif.package
        while package:
            if package.name:
                result = package.name.lower() + "_" + result
            package = package.package
            
        return result

    def _hasPrivateAttrs(self, inClass):

        return bool([attr for attr in inClass.attrs 
                     if attr.visi == PRIVATE and attr.scope == INSTANCE])

    def _hasProtectedAttrs(self, inClass):

        return bool([attr for attr in inClass.attrs 
                     if attr.visi == PROTECTED and attr.scope == INSTANCE])

    def _hasProtectedMethods(self, inClass):

        res = bool([m for m in inClass.methods if m.visi == PROTECTED])
        
        if not res:
            for m in self._overwrittenMethods(inClass):
                if m.visi == PROTECTED:
                    res = True
                    break
                            
        return res
    
    def _hasWriteProperties(self, inClass):
        
        for prop in inClass.props:
            if prop.access in [PROP_ACCESS_CONSTRUCTOR, PROP_ACCESS_READ_WRITE]:
                return True
        return False
    
    def _getMethodInfo(self, inScope, inIntfSymbol):
        
        intf = inScope.getSymbol(inIntfSymbol)
        
        return intf.getMethodInfo()

    def _initClassScope(self, inScope, inClass, inUserCode):
        
        self._initCommon(inScope, inUserCode)
        
        inScope.addSymbol("class", inClass)
        inScope.addSymbol("Classname", inClass.absName())
        inScope.addSymbol("classname", inClass.absName().lower())
        inScope.addSymbol("CLASSNAME", inClass.absName().upper())
        inScope.addSymbol("Classname_", inClass.absName().capitalize())
        inScope.addSymbol("NAMESPACE", self._packagePrefix(None, inClass).upper())
        inScope.addSymbol("withNamespace", bool(self._packagePrefix(None, inClass).upper()))
        inScope.addSymbol("Namespace", self._packagePrefix)
        inScope.addSymbol("BASENAME", inClass.name.upper())
        inScope.addSymbol("prefix", inClass.prefix().lower())
        inScope.addSymbol("_prefix", self._prefix)
        inScope.addSymbol("hasSuperClass", bool(inClass.superClass))
        
        if inClass.superClass:
            super = inClass.superClass
            inScope.addSymbol("Super", super.absName())
            inScope.addSymbol("super", super.absName().lower())
            inScope.addSymbol("superPrefix", super.prefix().lower())
            inScope.addSymbol("withSuperNamespace", bool(self._packagePrefix(None, super)))
            inScope.addSymbol("SUPER_NAMESPACE", self._packagePrefix(None, super).upper())
            inScope.addSymbol("SUPER_BASENAME", super.name.upper())

        inScope.addSymbol("hasConstructorArgs", bool(inClass.constructor.params))
        inScope.addSymbol("isConstructor", self._isConstructor)
        inScope.addSymbol("propertyInitArgs", self._propertyInitArgs(inClass))
        inScope.addSymbol("signature", self._signature)
        inScope.addSymbol("hasPrivAttrs", self._hasPrivateAttrs(inClass))
        inScope.addSymbol("hasProtAttrs", self._hasProtectedAttrs(inClass))
        inScope.addSymbol("hasProtMethods", self._hasProtectedMethods(inClass))
        inScope.addSymbol("hasSignals", bool([m for m in inClass.methods if m.isSignal]))
        inScope.addSymbol("hasProperties", bool(inClass.props))
        inScope.addSymbol("hasWriteProperties", self._hasWriteProperties(inClass))
        inScope.addSymbol("redefinedMethods", self._overwrittenMethods(inClass))
        inScope.addSymbol("castDefiningClass", self._castDefiningClass)
        inScope.addSymbol("interfaceClass", self._interfaceClass)
        inScope.addSymbol("interfaceType", self._interfaceType)
        inScope.addSymbol("classType", self._interfaceType)
        inScope.addSymbol("defaultProp", self._defaultProp)
        inScope.addSymbol("minProp", self._minProp)
        inScope.addSymbol("maxProp", self._maxProp)
        
        inScope.addSymbol("allInterfaces", self._allInterfaces(inClass))
        inScope.addSymbol("getMethodInfo", self._getMethodInfo)
                
        inScope.addSymbol("marshallerArgs", self._marshallerArgs)
        inScope.addSymbol("marshallerHasArgs", self._marshallerHasArgs)
        inScope.addSymbol("marshallerName", self._marshallerName)
        inScope.addSymbol("marshallerNumArgs", self._marshallerNumArgs)
        inScope.addSymbol("marshallerResult", self._marshallerResult)
        
        self._initClassTypeDependencies(inScope, inClass)
        
    def _initCommon(self, inScope, inUserCode):
        
        inScope.set_user_code(inUserCode)

        inScope.addSymbol("lower", self._lower)
        inScope.addSymbol("upper", self._upper)
        inScope.addSymbol("filename", self._filename)
        
        inScope.addSymbol("PRIVATE", PRIVATE)
        inScope.addSymbol("PROTECTED", PROTECTED)
        inScope.addSymbol("PUBLIC", PUBLIC)
        inScope.addSymbol("STATIC", STATIC)
        inScope.addSymbol("INSTANCE", INSTANCE)
        
        inScope.addSymbol("annotation", self._annotation)
        
    def _initClassTypeDependencies(self, inScope, inClass):
        
        headerFiles = []
        
        for attr in inClass.attrs:
            if not attr.visi == PUBLIC:
                continue
            if attr.typeObj and not inClass.inheritsFrom(attr.typeObj):
                self._appendHeaderDep(headerFiles, attr.typeObj)
                    
        for method in inClass.methods:
            if not method.visi == PUBLIC:
                continue
            if method.result.typeObj and not inClass.inheritsFrom(method.result.typeObj):
                self._appendHeaderDep(headerFiles, method.result.typeObj)
            for param in method.params:
                if param.typeObj and not inClass.inheritsFrom(param.typeObj):
                    self._appendHeaderDep(headerFiles, param.typeObj)
                    
        inScope.addSymbol("depHeaders", headerFiles)

    def _initIntfTypeDependencies(self, inScope, inIntf):
        
        headerFiles = []
        
        for method in inIntf.methods:
            if not method.visi == PUBLIC:
                continue
            if method.result.typeObj:
                self._appendHeaderDep(headerFiles, method.result.typeObj)
            for param in method.params:
                if param.typeObj:
                    self._appendHeaderDep(headerFiles, param.typeObj)
                    
        inScope.addSymbol("depHeaders", headerFiles)
                                    
    def _appendHeaderDep(self, inHeaderFiles, inTypeObj):
        
        obj = inTypeObj 
        
        if isinstance(obj, Class) or \
           isinstance(obj, Interface) or \
           isinstance(obj, Enumeration):
            
            headerFile = self._filename(None, obj) + ".h"
            if not headerFile in inHeaderFiles:
                inHeaderFiles.append(headerFile)
                
    def _initEnumerationScope(self, inScope, inEnum):
        
        self._initCommon(inScope, None)
        
        inScope.addSymbol("enum", inEnum)
        inScope.addSymbol("EnumAbsName", inEnum.absoluteName)
        inScope.addSymbol("ENUM_ABS_NAME", 
                          self._camelCaseToUnderScore(inEnum.absoluteName).upper()
                          )
        inScope.addSymbol("NAMESPACE", self._packagePrefix(None, inEnum).upper())
        inScope.addSymbol("withNamespace", bool(self._packagePrefix(None, inEnum).upper()))
        inScope.addSymbol("BASENAME", inEnum.name.upper())
        inScope.addSymbol("prefix", inEnum.prefix().lower())
        inScope.addSymbol("numCodes", str(len(inEnum.codes)))
        
    def _initErrorDomainScope(self, inScope, inErrorDomain, inUserCode):
        
        inScope.set_user_code(inUserCode)
        
        inScope.addSymbol("filename", self._filename)

        inScope.addSymbol("errorDomain", inErrorDomain)
        
        namespace = self._packagePrefix(None, inErrorDomain)
        error_domain_name = namespace + "_" + self._camelCaseToUnderScore(inErrorDomain.name)
        
        errorDomainName = inErrorDomain.name
        package = inErrorDomain.package
        while package:
            errorDomainName = package.name + errorDomainName
            package = package.package
        
        inScope.addSymbol("ERROR_DOMAIN_NAME", error_domain_name.upper())
        inScope.addSymbol("error_domain_name", error_domain_name.lower())
        inScope.addSymbol("ErrorDomainName", errorDomainName)
        
    def _initIntfScope(self, inScope, inIntf, inUserCode):
        
        self._initCommon(inScope, inUserCode)
 
        inScope.addSymbol("intf", inIntf)
        inScope.addSymbol("Intfname", inIntf.absName())
        inScope.addSymbol("intfname", inIntf.absName().lower())
        inScope.addSymbol("INTFNAME", inIntf.absName().upper())
        inScope.addSymbol("NAMESPACE", self._packagePrefix(None, inIntf).upper())
        inScope.addSymbol("withNamespace", bool(self._packagePrefix(None, inIntf).upper()))
        inScope.addSymbol("Namespace", self._packagePrefix)
        inScope.addSymbol("BASENAME", inIntf.name.upper())
        inScope.addSymbol("prefix", inIntf.prefix().lower())
        
        extendedIntfs = inIntf.getExtendedIntfs(inRecursive=False).values()
        inScope.addSymbol("extendedIntfs", extendedIntfs)
        inScope.addSymbol("hasExtendedIntfs", bool(extendedIntfs))
        allMethods = [info.method for info in inIntf.getMethodInfo()]
        inScope.addSymbol("allMethods", allMethods)
        
        inScope.addSymbol("signature", self._signature)
        
        self._initIntfTypeDependencies(inScope, inIntf)
                
    def _interfaceClass(self, inScope, inIntf):

        intf = inScope.getSymbol(inIntf)
        namespace = self._packagePrefix(None, intf).upper()
        basename = intf.name.upper()
        if not namespace:
            return "%s_CLASS" % basename
        else:
            return "%s_%s_CLASS" % (namespace, basename)

    def _interfaceType(self, inScope, inIntf):

        intf = inScope.getSymbol(inIntf)
        namespace = self._packagePrefix(None, intf).upper()
        basename = intf.name.upper()
        if not namespace:
            return "TYPE_%s" % basename
        else:
            return "%s_TYPE_%s" % (namespace, basename)   
        
    def _isConstructor(self, inScope, inClass, inMethod):
        
        cls = inScope.getSymbol(inClass)
        meth = inScope.getSymbol(inMethod)
        
        return meth is cls.constructor
        
    def _lower(self, inScope, inText):

        return inText.lower()
    
    def _marshallerArgs(self, inScope, inClassSymbol, inMethodSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        method = inScope.getSymbol(inMethodSymbol)
        
        mg = MarshallerGenerator(cls)
        
        return mg.getArgsGTypes(method)

    def _marshallerHasArgs(self, inScope, inClassSymbol, inMethodSymbol):
        
        return bool(self._marshallerArgs(inScope, inClassSymbol, inMethodSymbol))
    
    def _marshallerName(self, inScope, inClassSymbol, inMethodSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        method = inScope.getSymbol(inMethodSymbol)
        
        mg = MarshallerGenerator(cls)
        
        return mg.getMarshallerName(method)

    def _marshallerNumArgs(self, inScope, inClassSymbol, inMethodSymbol):
        
        return str(len(self._marshallerArgs(inScope, inClassSymbol, inMethodSymbol)))
            
    def _marshallerResult(self, inScope, inClassSymbol, inMethodSymbol):
        
        cls = inScope.getSymbol(inClassSymbol)
        method = inScope.getSymbol(inMethodSymbol)
        
        mg = MarshallerGenerator(cls)
        
        return mg.getResultGType(method)
    
    def _maxProp(self, inScope, inProperty):

        prop = inScope.getSymbol(inProperty)
        defaults = {
            PROP_INT : "G_MAXINT",
            PROP_DOUBLE : "G_MAXDOUBLE"
        }

        return self._propValueToString(prop.max, prop.type_, defaults)
    
    def _minProp(self, inScope, inProperty):

        prop = inScope.getSymbol(inProperty)
        defaults = {
            PROP_INT : "0",
            PROP_DOUBLE : "0.0",
        }

        return self._propValueToString(prop.min, prop.type_, defaults)
    
    def _overwrittenMethods(self, inClass):

        return [item[0] for item in inClass.overwritten]
    
    def _packagePrefix(self, inScope, inClif):

        result = ""
        
        if not inScope:
            clif = inClif
        else:
            clif = inScope.getSymbol(inClif)

        package = clif.package
        while package:
            if result and package.name:
                result = "_" + result
            result = package.name + result
            package = package.package
            
        return result
    
    def _prefix(self, inScope, inClifName):
        
        return inScope.getSymbol(inClifName).prefix().lower()
    
    def _propertyInitArgs(self, inClass):
        
        res = ""
        
        for name, value in inClass.prop_inits.items():
            if res:
                res += ", "
            res += '"%s", %s' % (name, value)
                    
        if res:
            res += ", "
        
        res += "NULL"
        
        return res
        
    def _propValueToString(self, inValue, inType, inDefaults={}):

        if inValue is not None:
            if inType == PROP_BOOLEAN:
                if inValue:
                    return "TRUE"
                else:
                    return "FALSE"
            elif inType == PROP_INT:
                return str(inValue)
            elif inType == PROP_DOUBLE:
                return str(inValue)
            elif inType == PROP_STRING:
                return '"%s"' % inValue
            elif inType == PROP_POINTER:
                raise GeneratorError
            elif inType == PROP_OBJECT:
                raise GeneratorError
            elif inType == PROP_ENUM:
                return str(inValue)
        else:
            return inDefaults[inType]

    def _signature(self,
                   inScope,
                   inMethod,
                   inWithTypes="True",
                   inWithNames="True",
                   inVertical="True"
                   ):

        result = ""

        method = inScope.getSymbol(inMethod)
        withTypes = (inWithTypes.capitalize() == "True")
        withNames = (inWithNames.capitalize() == "True")
        vertical = (inVertical.capitalize() == "True")

        if method.scope == INSTANCE:
            if withTypes:
                result += "%s*" % method.clif.absName()
            if withNames:
                if not isinstance(method.clif, Interface):
                    result += " self"
                else:
                    result += " object"
        for param in method.params:
            if result:
                result += ", "
                if vertical:
                    result += "\n\t"
            if not isinstance(param, VarParam):
                if withTypes:
                    result += param.type_
                if withNames:
                    if withTypes:
                        result += " "
                    result += param.name
            else:
                result += "..."

        if method.params and vertical:
            result += "\n\t"

        return result

    def _templatePath(self, inTemplName):

        outPath = Generator._DIR + os.sep + "templates" 
        outPath += os.sep + inTemplName

        return outPath

    def _upper(self, inScope, inText):

        return inText.upper()

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
        
class GeneratorError(Exception):
    
    pass
