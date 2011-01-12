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

import os
from .usercode import UserCode

class GeneratorError(Exception): pass

class GeneratorErrorAbstractClass(GeneratorError): pass

class _GenInput(object):
    
    def __init__(self):
        if self.__class__ is _GenInput:
            raise GeneratorErrorAbstractClass
        
    def getUserCode(self, inName):
        """
        liefert UserCode zu Datei
        """
        return None
    
class _GenOutput(object):
    
    def __init__(self):
        if self.__class__ is _GenOutput:
            raise GeneratorErrorAbstractClass
    
    def open(self, inName):
        """
        öffnet Ausgabe
        """
        pass
    
    def writeCode(self, inLines):
        
        lines = self._remove_duplicate_empty_lines(inLines)
        
        self._writeCode(lines)
        
    def close(self):
        pass

    def _writeCode(self, inLines):
        pass

    def _remove_duplicate_empty_lines(self, inLines):
        
        result = []
        last_line_empty = False
        
        for line in inLines:
            if not line.strip() == "":
                result.append(line)
                last_line_empty = False
            elif not last_line_empty:
                result.append(line)
                last_line_empty = True
            
        return result
    
class GenInputNull(_GenInput):

    def __init__(self):
        
        _GenInput.__init__(self)

class GenInputDir(_GenInput):
    
    def __init__(self, inDir = "."):
        
        _GenInput.__init__(self)
        self._dir = inDir 

    def getUserCode(self, inName):
        
        filename = self._dir + os.sep + inName
        
        return UserCode.createFromFile(filename)

class GenOutputStd(_GenOutput):

    def __init__(self):
        
        _GenOutput.__init__(self)
        
    def open(self, inName):
        
        print(">" * 10 + " %s " % inName + ">" * 10)
        
    def close(self):
        
        print("<" * 20)
        print()
        
    def _writeCode(self, inLines):
        
        for line in lines:
            print(line)

class GenOutputDir(_GenOutput):

    def __init__(self, inDir = ".", inVerbose = False):
        
        _GenOutput.__init__(self)
        self._dir = inDir
        self._verbose = inVerbose
        
        # Verzeichnis erzeugen, sofern noch nicht vorhanden:
        try:
            os.makedirs(self._dir)
        except os.error:
            pass    
        
    def open(self, inName):
        
        filename = self._dir + os.sep + inName
        self._file = open(filename, "w")
        
        if self._verbose:
            print("Generating file %s ..." % filename, end=' ')
                
    def close(self):
        
        self._file.close()
        
        if self._verbose:
            print("done")
                
    def _writeCode(self, inLines):
        
        for line in inLines:
            self._file.write(line + "\n")
