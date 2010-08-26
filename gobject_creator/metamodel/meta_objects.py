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

import inspect
import os.path

class _WithContext(object):
    
    def __enter__(self):
       
        _push(self)
        return self
    
    def __exit__(self, inExcType, inExcValue, inTraceback):
      
        _pop()
        return False

class DefinitionError(Exception): pass

class _PackageComponent(object):
    
    def __init__(self, inName, inAlias=""):
        
        self.name = inName
        if inAlias:
            self.alias = inAlias
        else:
            self.alias = self.name
        self._package = None
        
        try:
            self.metadef_file = os.path.abspath(inspect.stack()[-1][1])
        except:
            self.metadef_file = None
            
    def getPackage(self):
    
        return self._package
    
    package = property(getPackage)
    
    def getAbsoluteName(self):
        
        res = self.name
        p = self.package
        while p:
            res = p.name.capitalize() + res
            p = p.package
            
        return res
    
    absoluteName = property(getAbsoluteName)

    def prefix(self):
        
        result = self.alias.lower()
        package = self._package
        while package:
            if package.name:
                result = package.name.lower() + "_" + result
            package = package._package
        return result
    
    def getGTypeName(self):
        
        res = "TYPE_" + self.name.upper()

        package = self._package
        while package:
            if package.name:
                res = package.name.upper() + "_" + res
            package = package._package
        
        return res
    
    gtypeName = property(getGTypeName)
        
class Package(_WithContext):
    
    """
    A package contains classes, interfaces, error domains and enumeration types.
    Objects in a package can be accessed by the "." notation. If e.g. class "Foo"
    is part of package "FooPack" it can be referred to as "FooPack.Foo".
    """
    
    __instances = {}
    
    def __init__(self, inName):
        """
        Returns a (new) package instance. The package class implements the
        multiton pattern: if a package has already been created for the given
        name the old and the new instance will share their internal data.
        
        --> inName:     Package name
        <--             Package
        
        """
        
        _WithContext.__init__(self)
        
        try:
            self.__dict__['_internal'] = Package.__instances[inName]
        except KeyError:
            Package.__instances[inName] = Package._InternalPack(inName, self)
             
    def __setattr__(self, inName, inValue):
        
        ownAttrNames = ['_internal', 
                        '_WithContext__enter__', 
                        '_WithContext__exit__']
        
        if inName not in ownAttrNames:
            setattr(self._internal, inName, inValue)
        else:
            setattr(self, inName, inValue)
    
    def __getattr__(self, inName):
        
        ownAttrNames = ['_internal', 
                        '_WithContext__enter__', 
                        '_WithContext__exit__']
        
        if inName not in ownAttrNames:
            return getattr(self.__dict__['_internal'], inName)
        else:
            return self.__dict__[inName]
                
    class _InternalPack(_PackageComponent):
    
        def __init__(self, inName, inOuterInstance):
            
            _PackageComponent.__init__(self, inName)
            
            self._outerInstance = inOuterInstance
            inOuterInstance.__dict__['_internal'] = self
     
            self.subPacks = {}
            self.classes = {}
            self.intfs = {}
            self.errorDomains = {}
            self.enums = {}
     
            parent = _getLast(Package)
            if parent:
                parent.addObject(self._outerInstance)
            else:
                ObjectCatalog.get().add_top_object(self._outerInstance)
                
        def addObject(self, inObj):
            
            if isinstance(inObj, Package):
                self.subPacks[inObj.name] = inObj
            elif isinstance(inObj, Class):
                self.classes[inObj.name] = inObj
            elif isinstance(inObj, Interface):
                self.intfs[inObj.name] = inObj
            elif isinstance(inObj, ErrorDomain):
                self.errorDomains[inObj.name] = inObj
            elif isinstance(inObj, Enumeration):
                self.enums[inObj.name] = inObj
            else:
                raise DefinitionError
             
            inObj._package = self
         
        def __getattr__(self, inName):
            
            if inName in self.subPacks:
                return self.subPacks[inName]
            elif inName in self.classes:
                return self.classes[inName]
            elif inName in self.intfs:
                return self.intfs[inName]
            elif inName in self.errorDomains:
                return self.errorDomains[inName]
            elif inName in self.enums:
                return self.enums[inName]
            else:
                raise AttributeError

class _Clif(_WithContext, _PackageComponent):
    
    def __init__(self, inName, inAlias=""):
        
        _WithContext.__init__(self)
        _PackageComponent.__init__(self, inName, inAlias)
        
        self.methods = []

        package = _getLast(Package)
        if package:
            package.addObject(self)
        else:
            ObjectCatalog.get().add_top_object(self)

        self.absName = self.getAbsoluteName # Alias aus Kompatibilitätsgründen
        
    
    def typeName(self):
        
        # TODO: Sprachabhängigkeit besser berücksichtigen
        return "%s*" % self.absoluteName

    def addMethod(self, inMethod):
        
        for m in self.methods:
            if m.name == inMethod.name:
                idx = self.methods.index(m)
                break
        else:
            idx = -1
            
        if idx == -1:
            self.methods.append(inMethod)
        else:
            self.methods[idx] = inMethod
            
        inMethod.clif = self
        
    def _usesVarArgsMethods(self):
        
        for meth in self.methods:
            for param in meth.params:
                if isinstance(param, VarParam):
                    return True
                
        return False
                
    usesVarArgsMethods = property(_usesVarArgsMethods)
        
    def __getattr__(self, inName):
        
        for m in self.methods:
            if m.name == inName:
                return m
        else:
            raise AttributeError, inName
        
class Interface(_Clif):
    
    def __init__(self, inName, inAlias=""):
        """
        Creates a new interface.
        
        --> inName:     Interface name
        --> inAlias:    Alias name. If given the alias name will be used
                        in the prefix of the interface's functions instead of
                        the interface name
        <--             Interface
        
        """
        
        _Clif.__init__(self, inName, inAlias)
        
        self._interfaces = {}
        
    def addInterface(self, inIntf):
        
        if inIntf in self._interfaces:
            raise DefinitionError
        
        self._interfaces[inIntf.name] = inIntf
        
    def getExtendedIntfs(self, inRecursive=False):
        
        if not inRecursive:
            return self._interfaces
        else:
            res = self._interfaces.copy()
            
            for intf in self._interfaces.values():
                res.update(intf.getExtendedIntfs(True))

            return res 
    
    def getMethodInfo(self):
        
        res = []
        
        methods = self._getAllMethods()
        for name in methods:
            info = IntfMethodInfo(name, methods[name][0], methods[name][1])
            res.append(info)
            
        res.sort()
            
        return res
    
    def _getAllMethods(self):
        """
        Info über Methoden als Dictionary im Format:
        { <methodenname> : (<methode>, <definierende Schnittstelle>) } 
        """
        res = {}
        for m in self.methods:
            res[m.name] = (m, self)
        
        for intf in self._interfaces.values():
            res.update(intf._getAllMethods())
            
        return res
    
class IntfMethodInfo:
    
    def __init__(self, inName, inMethod, inDefiningIntf):
              
        self.name = inName
        self.method = inMethod
        self.definingIntf = inDefiningIntf
        
    def __cmp__(self, inOther):
        
        if isinstance(inOther, IntfMethodInfo):
            val1 = self.name
            val2 = inOther.name
        else:
            val1 = id(self)
            val2 = id(inOther) 
        
        if val1 < val2:
            return -1
        elif val1 > val2:
            return 1
        else:
            return 0
                
class Class(_Clif):
    
    _CONSTRUCTOR_NAME = "new"
    
    def __init__(self, inName, inSuperClass = None, inAlias="",
                 inAbstract = False):
        """
        Creates a new class.
        
        --> inName:         Class name
        --> inSuperClass:   Super class instance
        --> inAlias:        Alias name. If given the alias name will be used
                            in the prefix of the classes functions instead of
                            the class name
        --> inAbstract:     If "True" the class will be defined as abstract
        <--                 Class
        
        """
        
        _Clif.__init__(self, inName, inAlias)
        
        self.superClass = inSuperClass

        self.intfImpls = []
        self.attrs = []
        self.props = []
        self.prop_inits = {} 
        self.overwritten = []
        self.abstract = inAbstract

        _push(self) # Klasse muss für Constructor() auf Stack liegen
        self.addMethod(Constructor())
        _pop()
        
        
    def getMethodInfo(self, inMethodName):
        """
        --> inMethodName : Name der Methode
        <-- Methode, Implementierende Klasse, Schnittstelle
        """
        
        names = inMethodName.split(".")
        methodName = names[-1]
        if len(names) > 1:
            intfName = "".join(names[:-1])
        else:
            intfName = ""
            
        cls = self
        while cls:
            if not intfName:
                for m in cls.methods:
                    if m.name == methodName:
                        return m, cls, None
                for intf in cls.intfImpls:
                    for m in intf.methods:
                        if m.name == methodName:
                            return m, cls, intf
            else:
                for intf in cls.intfImpls:
                    if intf.absName() != intfName:
                        continue
                    for m in intf.methods:
                        if m.name == methodName:
                            return m, cls, intf
            cls = cls.superClass
                
        return None, None, None
        
    def addAttribute(self, inAttr):
        
        self.attrs.append(inAttr)
        
    def addProperty(self, inProperty):
        
        self.props.append(inProperty)
        
    def implement(self, inIntf):
        
        self.intfImpls.append(inIntf)
        
    def overwrite(self, inMethodName):
        
        method, cls, intf = self.getMethodInfo(inMethodName)
        
        if method is None:
            raise DefinitionError
        
        if ( not method.virtual ) or ( method.visi == PRIVATE ) or \
           ( method.scope == STATIC ):
            raise DefinitionError       
        
        if cls is self:
            raise DefinitionError
        
        self.overwritten.append((method, intf))
        
    def inheritsFrom(self, inOtherClass):
        
        if not isinstance(inOtherClass, Class):
            return False
        
        cls = self.superClass
        while cls:
            if cls is inOtherClass:
                return True
            cls = cls.superClass
        return False
        
class ErrorDomain(_WithContext, _PackageComponent):
    
    def __init__(self, inName):
        """
        Creates a new error domain.
        
        --> inName: Name of error domain
        <--         Error domain
        
        """
        
        _WithContext.__init__(self)
        _PackageComponent.__init__(self, inName)
        
        self.errorCodeNames = []
        self.errorCodes = []
                
        package = _getLast(Package)
        if package:
            package.addObject(self)
        else:
            ObjectCatalog.get().add_top_object(self)
    
    def addErrorCode(self, inErrorCode):
        
        self.errorCodeNames.append(inErrorCode.codeName)
        self.errorCodes.append(inErrorCode)
    
class ErrorCode(object):
    
    def __init__(self, inCodeName):
        
        domain = _getLast()
        if not isinstance(domain, ErrorDomain):
            raise DefinitionError
        
        self.codeName = inCodeName
        
        domain.addErrorCode(self)

class Enumeration(_WithContext, _PackageComponent):
    
    def __init__(self, inName, inIsFlagType=False):
        
        _WithContext.__init__(self)
        _PackageComponent.__init__(self, inName)
        
        self.codes = []
        self.isFlagType = inIsFlagType
               
        package = _getLast(Package)
        if package:
            package.addObject(self)
        else:
            ObjectCatalog.get().add_top_object(self)
            
    def addCode(self, inCode):
        
        self.codes.append(inCode)
        
    def typeName(self):
        
        # TODO: Sprachabhängigkeit besser berücksichtigen
        if not self.isFlagType:
            return self.absoluteName
        else:
            return self.absoluteName + "Flags"
        
    def __getattr__(self, inName):
        
        for code in self.codes:
            if code.name == inName:
                return code
        raise AttributeError
    
class EnumCode(object):
    
    def __init__(self, inName, inValue=-1):
        
        enum = _getLast()
        if not isinstance(enum, Enumeration):
            raise DefinitionError
        
        self.name = inName
        
        if not enum.isFlagType:
            self.value = str(inValue)
            self.valueGiven = bool(inValue > 0)
        else:
            self.value = len(enum.codes) # <- Operand für Links-Shift-Operator
            self.valueGiven = True
                  
        enum.addCode(self)
        self.enum = enum
        
    def codeName(self):
        
        # TODO: Sprachabhängigkeit berücksichtigen:        
        res = self._camelCaseToUnderScore(self.enum.absoluteName).upper()
        res += "_" + self.name
        
        return res
    
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
    
class Implements(object):
    
    def __init__(self, inIntf):
        
        cls = _getLast()
        if not isinstance(cls, Class):
            raise DefinitionError
        
        cls.implement(inIntf)
        
class Extends(object):
    
    def __init__(self, inIntf):
        
        intf = _getLast()
        if not isinstance(intf, Interface):
            raise DefinitionError
        
        intf.addInterface(inIntf)
          
class Overwrite(object):
    
    def __init__(self, inMethodName):

        cls = _getLast()
        if not isinstance(cls, Class):
            raise DefinitionError
        
        cls.overwrite(inMethodName)
        
Override = Overwrite # Alias
        
PUBLIC, PROTECTED, PRIVATE = range(1, 4)
    
INSTANCE, STATIC = range(1, 3)

class Value(object):
    
    def __init__(self, inName, inType):
        
        self.name = inName
        if isinstance(inType, str):
            self.type_ = inType
            self._typeObj = None
        else:
            self.type_ = inType.typeName()
            self._typeObj = inType
            
    def _getTypeObject(self):
        return self._typeObj
    
    typeObj = property(_getTypeObject)

class Attr(Value):
    
    def __init__(self,
        inName,
        inType,
        inScope = INSTANCE,
        inVisi = PRIVATE,
        inInitValue = None
        ):
        
        Value.__init__(self, inName, inType)
        
        self.scope = inScope
        self.visi = inVisi
        if self.scope == INSTANCE:
            self.initValue = None
        else:
            if inInitValue is not None:
                self.initValue = str(inInitValue)
            else:
                self.initValue = None
        
        cls = _getLast()
        if not isinstance(cls, Class):
            raise DefinitionError
        cls.addAttribute(self)

class StaticAttr(Attr):
    
    def __init__(self,
        inName,
        inType,
        inVisi = PRIVATE,
        inInitValue = None
        ):
        
        Attr.__init__(self, inName, inType, STATIC, 
                      inVisi, inInitValue)
                
PROP_BOOLEAN, \
PROP_INT, \
PROP_DOUBLE, \
PROP_STRING, \
PROP_POINTER, \
PROP_OBJECT, \
PROP_ENUM = range(7)

PROP_ACCESS_READ, \
PROP_ACCESS_CONSTRUCTOR, \
PROP_ACCESS_READ_WRITE = range(3)

class Property(object):
    
    def __init__(self, 
                 inName, 
                 inDescr, 
                 inType = PROP_STRING,
                 inAccess = PROP_ACCESS_READ,
                 inMin = None,
                 inMax = None,
                 inDefault = None,
                 inGObjectType = ""
                 ):
        
        self.name = inName
        self.descr = inDescr
        self.type_ = inType
        self.access = inAccess
        self.min = inMin
        self.max = inMax

        if isinstance(inDefault, EnumCode):
            self.default = inDefault.codeName()
        else:
            self.default = inDefault

        if isinstance(inGObjectType, _PackageComponent):
            self.gobjectType = inGObjectType.gtypeName
        else:
            self.gobjectType = inGObjectType
        
        if self.type_ == PROP_OBJECT or self.type_ == PROP_ENUM:
            if not self.gobjectType:
                raise DefinitionError
        
        cls = _getLast()
        if not isinstance(cls, Class):
            raise DefinitionError
        cls.addProperty(self)
        
    def _varname(self):
        return self.name.replace("-", "_")
    varname = property(_varname)        
    
class Param(Value):
    
    def __init__(self, 
                 inName, 
                 inType,
                 ):
        
        Value.__init__(self, inName, inType)
        
        self.method = None
       
        m = _getLast()
        if isinstance(m, Method):
            if not isinstance(self, Result):
                m.addParam(self)
            else:
                m.result = self
                self.method = m
        
class Result(Param):
    
    def __init__(self, inType):
        
        Param.__init__(self, "", inType)
        
class ConstructorParam(Param):
    
    def __init__(self,
                 inName,
                 inType
                 ):
        
        Param.__init__(self, inName, inType)
                
    def BindProperty(self, inPropertyName):
        
        try:
            method = _getLast()
            cls = method.clif
            if not cls.constructor is method:
                raise DefinitionError
        except:
            raise DefinitionError
        
        cls.prop_inits[inPropertyName] = self.name
               
class InitProperty(object):
    
    def __init__(self, inPropertyName, inPropertyValue):
        
        try:
            method = _getLast()
            cls = method.clif
            if not cls.constructor is method:
                raise DefinitionError
        except:
            raise DefinitionError
        
        if isinstance(inPropertyValue, str):
            value = inPropertyValue
        else:
            value = inPropertyValue.codeName()
        
        cls.prop_inits[inPropertyName] = value
  
class VarParam(Param):
    
    def __init__(self):
        
        Param.__init__(self, "", "")
                        
class Method(_WithContext):
    
    def __init__(self, 
        inName, 
        inResultType = "void",
        inScope = INSTANCE,
        inVisi = PRIVATE,
        inVirtual = False,
        inAbstract = False,
        inIsSignal = False,
        inResultParam = None
        ):
        
        _WithContext.__init__(self)
        
        self.name = inName
        
        if inResultParam is None:
            self.result = Result(inResultType) 
        else:
            self.result = inResultParam
        self.result.method = self
        
        self.scope = inScope
        self.visi = inVisi
        self.abstract = inAbstract
        if self.abstract:
            self.virtual = True
        else:
            self.virtual = inVirtual
            
        self.isSignal = inIsSignal
        
        self.params = []
        
        clif = _getLast()
        if isinstance(clif, Interface):
            if ( not self.scope == INSTANCE ) or \
               ( not self.visi == PUBLIC ) or \
               ( not self.virtual ):
               
                raise DefinitionError
            
        clif.addMethod(self)
        
    def accept(self, inVisitor):
        
        inVisitor.onMethodBegin(self)
        
        for param in self.params:
            inVisitor.onParameter(param)
            
        inVisitor.onMethodEnd(self)
        
    def _getResultType(self):

        return self.result.type_

    resultType = property(_getResultType)
        
    def addParam(self, inParam):
        
        self.params.append(inParam)
        inParam.method = self

class StaticMethod(Method):
    
    def __init__(self, 
        inName, 
        inResultType = "void",
        inVisi = PRIVATE,
        inResultParam = None
        ):
        
        Method.__init__(self, inName, inResultType, STATIC, 
            inVisi, False, inResultParam = inResultParam)
        
class Signal(Method):
    
    def __init__(self,
                 inName,
                 inResultType = "void"
                 ):
        
        methodName = ""
        for ch in inName:
            if not ch == "-":
                methodName += ch
            else:
                methodName += "_"
            
        Method.__init__(self, methodName, inResultType, inScope=INSTANCE,
                        inVisi=PUBLIC, inAbstract=True, inIsSignal=True)
        
        self.signalName = inName
        
    def accept(self, inVisitor):
        
        inVisitor.onSignalBegin(self)
        
        for param in self.params:
            inVisitor.onParameter(param)
            
        inVisitor.onSignalEnd(self)
        
class Constructor(StaticMethod):
    
    def __init__(self):

        cls = _getLast()
        if not isinstance(cls, Class):
            raise DefinitionError
        
        result = Result("%s*" % cls.absoluteName)
 
        StaticMethod.__init__(self, 
                              Class._CONSTRUCTOR_NAME, 
                              inVisi = PUBLIC,
                              inResultParam = result
                              )
            
        cls.constructor = self
        self._cls = cls
 
class IntfMethod(Method):
    
    def __init__(self, 
        inName, 
        inResultType = "void",
        inResultParam = None
        ):
        
        if not isinstance(_getLast(), Interface):
            raise DefinitionError
        
        Method.__init__(self, inName, inResultType, inScope = INSTANCE,
            inVisi = PUBLIC, inAbstract = True, inResultParam = inResultParam)

_g_stack = []

def _getLast(inType = None):
    
    minIdx = -len(_g_stack)
    idx = -1
    while idx >= minIdx:
        obj = _g_stack[idx]
        if inType is None:
            return obj
        elif isinstance(obj, inType):
            return obj
        else:
            idx -= 1
    return None

def _push(inObj):
    
    _g_stack.append(inObj)
    
def _pop():
    
    try:
        return _g_stack.pop()
    except IndexError:
        return None

from metamodel.object_catalog import ObjectCatalog
