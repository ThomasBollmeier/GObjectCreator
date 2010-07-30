# coding=UTF-8

class IPackageVisitor:
    
    def onPackageBegin(self, inPackage):
        raise NotImplementedError
    
    def onPackageEnd(self, inPackage):
        raise NotImplementedError
    
    def onClassBegin(self, inClass):
        raise NotImplementedError

    def onClassEnd(self, inClass):
        raise NotImplementedError

    def onInterfaceBegin(self, inIntf):
        raise NotImplementedError

    def onInterfaceEnd(self, inIntf):
        raise NotImplementedError
    
    def onErrorDomainBegin(self, inErrorDomain):
        raise NotImplementedError

    def onErrorDomainEnd(self, inErrorDomain):
        raise NotImplementedError
    
    def onAttribute(self, inAttr):
        raise NotImplementedError
    
    def onProperty(self, inProp):
        raise NotImplementedError
    
    def onMethodBegin(self, inMethod):
        raise NotImplementedError

    def onMethodEnd(self, inMethod):
        raise NotImplementedError

    def onSignalBegin(self, inSignal):
        raise NotImplementedError

    def onSignalEnd(self, inSignal):
        raise NotImplementedError
    
    def onParameter(self, inParam):
        raise NotImplementedError
    
    def onErrorCode(self, inErrorCode):
        raise NotImplementedError
   