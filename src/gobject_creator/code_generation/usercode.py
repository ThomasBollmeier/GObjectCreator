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

import re

class UserCode(object):
    
    STYLES = COMMENT_C, COMMENT_CPP = range(2)
    _begin = r"\s*/\*\s*UserCode\s+(\w*)\s*{\s*\*/"
    _end = r"\s*/\*\s*}\s*UserCode\s*\*/"
    _style = COMMENT_C
    
    def __init__(self):
        self._re_block_begin = re.compile(UserCode._begin)
        self._re_block_end = re.compile(UserCode._end)
        self.__mth_blocks = {}
        
    @staticmethod
    def setCommentStyle(inStyle):
        
        if inStyle == UserCode.COMMENT_C:
            UserCode._begin = r"\s*/\*\s*UserCode\s+(\w*)\s*{\s*\*/"
            UserCode._end = r"\s*/\*\s*}\s*UserCode\s*\*/"
        elif inStyle == UserCode.COMMENT_CPP:
            UserCode._begin = r"\s*//\s*UserCode\s+(\w*)\s*{\s*"
            UserCode._end = r"\s*//\s*}\s*UserCode\s*"
        else:
            return
        
        UserCode._style = inStyle
        
    @staticmethod
    def createFromFile( in_filename ):
        out_userCode = UserCode()
        out_userCode.__parse( in_filename )
        return out_userCode
    

    def isEmpty(self, inBlockname):

        return ( inBlockname not in self.__mth_blocks )

    def setDefaultCode(self, inBlockname, inLines):
        
        if inBlockname in self.__mth_blocks:
            return

        lines = [self.__blockBegin(inBlockname)]
        lines += inLines[:] 
        lines.append(self.__blockEnd())
        
        self.__mth_blocks[inBlockname] = lines
    
    def __call__(self,
                 io_scope,
                 iv_blockname
                 ):
        rv_codestr = ""
        lt_lines = self.__getBlock( iv_blockname )
        for lv_line in lt_lines:
            if rv_codestr:
                rv_codestr += "\n"
            rv_codestr += lv_line
        return rv_codestr
    
    def __blockBegin(self, inBlockname):
        
        if UserCode._style == UserCode.COMMENT_C:
            result = "/* UserCode %s { */" % inBlockname
        elif UserCode._style == UserCode.COMMENT_CPP:
            result = "// UserCode %s {" % inBlockname
        
        return result
    
    def __blockEnd(self):

        if UserCode._style == UserCode.COMMENT_C:
            result = "/* } UserCode */"
        elif UserCode._style == UserCode.COMMENT_CPP:
            result = "// } UserCode"
        
        return result
 
    def __isBlockBegin(self, inLine):
        
        match = self._re_block_begin.match(inLine)
        if match:
            return True, match.group(1)
        else:
            return False, ""

    def __isBlockEnd(self, inLine):
        
        match = self._re_block_end.match(inLine)
        if match:
            return True
        else:
            return False
    
    def __getBlock(self,
                   iv_blockname
                   ):
        try:
            rt_lines = self.__mth_blocks[iv_blockname][:]
        except KeyError:
            rt_lines = self.__createBlock( iv_blockname )
        return rt_lines
    
    def __parse(self, 
                iv_filename
                ):
        
        self.__mth_blocks = {}
        
        try:
            inputFile = open( iv_filename, "r" )
        except IOError:
            return
        lines = inputFile.readlines()
        inputFile.close()
        
        codeblock = False
        
        for line in lines:
            
            line = line[:-1] # Zeilenumbruch entfernen
            
            if not codeblock:
                blockbegin, blockname = self.__isBlockBegin(line)
                if blockbegin:
                    codeblock = True
                    userlines = []
            else:
                if not self.__isBlockEnd(line):
                    userlines.append(line)
                else:
                    self.setDefaultCode(blockname, userlines)
                    codeblock = False
                    blockname = ""

    def __createBlock(self,
                      iv_blockname
                      ):

        rt_lines = [self.__blockBegin(iv_blockname)]

        if UserCode._style == UserCode.COMMENT_C:
            rt_lines.append( "/* insert code here ... */" )
        elif UserCode._style == UserCode.COMMENT_CPP:
            rt_lines.append( "// insert code here ..." )
                
        rt_lines.append( self.__blockEnd())
        self.__mth_blocks[iv_blockname] = rt_lines
        
        return rt_lines
    
if __name__ == "__main__":
        
    line = "  /*     UserCode Test { */"
    begin, blockname = UserCode()._UserCode__isBlockBegin(line)
    if begin:
        print '"%s"' % blockname
        
    line = "/*}UserCode*/"
    print UserCode()._UserCode__isBlockEnd(line)
        
    
