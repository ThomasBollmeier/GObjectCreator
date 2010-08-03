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
   