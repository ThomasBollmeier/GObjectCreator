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

from .scope import *
from .components import *
import re

class ParseError(Exception):
    pass

def is_empty_table( io_scope, 
                    iv_table
                    ):
    lt_rows = io_scope.getSymbol( iv_table )
    return len( lt_rows ) == 0

def is_first( io_scope ):
    return io_scope.getIndex() == 0

def is_last( io_scope ):
    return io_scope.getIndex() == io_scope.getMaxIndex()

def is_equal( io_scope,
              iv_value1,
              iv_value2
              ):
    
    if _is_literal( iv_value1 ):
        lv_val1 = iv_value1[1:-1]
    else:
        lv_val1 = io_scope.getSymbolStr( iv_value1 )

    if _is_literal( iv_value2 ):
        lv_val2 = iv_value2[1:-1]
    else:
        lv_val2 = io_scope.getSymbolStr( iv_value2 )
        
    return lv_val1 == lv_val2

def _is_literal( iv_value ):
    if len( iv_value ) <= 2:
        return False
    lt_chars = [ "'", '"' ]
    if iv_value[0] in lt_chars and iv_value[-1] in lt_chars:
        return True
    else:
        return False

class Parser(object):        
    
    _go_regex_cmd = re.compile( r"#![ \s]*(.+)" )
    
    def __init__(self, 
                 io_scope
                 ):
        
        self.mo_scope = io_scope
        self.mo_scope.addSymbol( "first", is_first )
        self.mo_scope.addSymbol( "last", is_last )
        self.mo_scope.addSymbol( "equal", is_equal )
        self.mo_scope.addSymbol( "empty", is_empty_table )
        
    def parseFile(self, 
                  iv_filename 
                  ):
        rt_codelines = []
        lo_code = self._readBlocksFromFile( iv_filename )
        return lo_code.getCode( io_scope = self.mo_scope )
    
    def parseLines(self,
                   it_lines
                   ):
        
        lo_code = self._readBlocks(it_lines)
        return lo_code.getCode( io_scope = self.mo_scope )
        
    def _readBlocksFromFile(self,
                            iv_filename
                            ):
        lo_file = open( iv_filename, "r" )
        lt_lines = [ lv_line.rstrip("\n") 
                    for lv_line in lo_file.readlines()
                    ]
        lo_file.close()
        
        return self._readBlocks( it_lines = lt_lines )
    
    def _readBlocks(self,
                    it_lines
                    ):
        
        ro_block = CodeBlock()
        lo_block = ro_block
        
        for lv_line in it_lines:
            lo_match = Parser._go_regex_cmd.search( lv_line )
            if lo_match == None:
                # Normale Zeile
                lo_block.addLine( iv_line = lv_line )
            else:
                # --> Befehls-/Steuerzeile
                lt_args = lo_match.group( 1 ).split()
                lv_command = lt_args[0].lower()
                lv_command.strip()
                try:
                    lt_args = lt_args[1:]
                except:
                    lt_args = []                
                if lv_command == "for":
                    lt_args, lo_whereExpr = self._splitForArgs(lt_args)
                    lv_numArgs = len( lt_args )
                    if lv_numArgs == 1:
                        # Befehlsversion: #! for [<liste>|<listfunktion> <arg1>, ...]
                        lv_table = lt_args[0]
                        lv_rowname = lv_table
                    elif lv_numArgs == 3:
                        # Befehlsversion: #! for <zeile> in [<liste>|<listfunktion> <arg1>, ...]
                        lv_table = lt_args[2]
                        lv_rowname = lt_args[0]
                    else:
                        raise ParseError
                    lo_new_block = ForBlock(
                        iv_table = lv_table,
                        iv_rowname = lv_rowname,
                        io_whereExpr = lo_whereExpr
                        )
                    lo_block.addComponent( io_comp = lo_new_block )
                    lo_block = lo_new_block
                elif lv_command in [ "if", "elif" ]:
                    lv_exprStr = " ".join(lt_args)
                    lo_boolExpr = BoolExpr( lv_exprStr )
                    if lv_command == "if":
                        lo_new_block = IfBlock( lo_boolExpr )
                        lo_block.addComponent( io_comp = lo_new_block )
                        lo_block = lo_new_block
                    else:
                        lo_block.addElif( lo_boolExpr )
                elif lv_command == "else":
                    lo_block.addElse()
                elif lv_command == "user_code":
                    # Befehl: #! user_code <Blockname>
                    lo_new_block = UserComponent(lt_args[0])
                    lo_block.addComponent(io_comp = lo_new_block)
                    lo_block = lo_new_block
                elif lv_command == "end":
                    lo_block = lo_block.mo_parent
                else:
                    raise ParseError
                        
        return ro_block

    def _splitForArgs(self, inArgs):
        
        hlp = [arg.upper() for arg in inArgs]
        
        try:
            idx = hlp.index("WHERE")
            begin = inArgs[:idx]
            outBoolExpr = BoolExpr(" ".join(inArgs[idx+1:]))
        except ValueError:
            begin = inArgs[:]
            outBoolExpr = None
                
        hlp = [arg.upper() for arg in begin]
        if "IN" in hlp:
            outArgs = begin[:2]
            if len(begin) == 3:
                outArgs.append(begin[2])
            else:
                outArgs.append(begin[2:])
        elif len(begin) == 1:
            outArgs = begin
        else:
            raise ParseError
        
        return outArgs, outBoolExpr
