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

from code_generation.translator import Translator
from code_generation.scope import ForScope
from code_generation.bool_parser import BoolParser

class NoUserCode(Exception):
    pass

class NotImplemented(Exception): 
    pass

class Component(object):
    
    def __init__(self):
        self.mo_parent = None
    
    def addLine(self,
                iv_line
                ):
        raise NotImplemented
    
    def getCode(self,
                io_scope
                ):
        raise NotImplemented
    
class CodeLines(Component):
    
    def __init__(self):
        Component.__init__( self )
        self.mt_lines = []
        
    def addLine(self,
                iv_line
                ):
        self.mt_lines.append( iv_line )

    def getCode(self,
                io_scope
                ):
        rt_codelines = []
        lo_translator = Translator( io_scope )
        for lv_line in self.mt_lines:
            lv_codeline = lo_translator.translate( lv_line )
            rt_codelines.append( lv_codeline )
        return rt_codelines
                
class CodeBlock(Component):

    def __init__(self):
        Component.__init__( self )
        lo_child = CodeLines()
        self.mt_children = [ lo_child ]
        lo_child.parent = self
        
    def addComponent(self,
                     io_comp
                     ):
        self.mt_children.append( io_comp )
        io_comp.mo_parent = self
        
    def addLine(self,
                iv_line
                ):
        lo_child = self.mt_children[-1]
        if not isinstance( lo_child, CodeLines ):
            lo_child = CodeLines()
            self.addComponent( io_comp = lo_child )
        lo_child.addLine( iv_line )

    def getCode(self,
                io_scope
                ):
        rt_codelines = []
        for lo_child in self.mt_children:
            rt_codelines += lo_child.getCode( io_scope )
        return rt_codelines
    
class _Evaluator(object):
    
    def __init__(self, io_scope):
        
        self.mo_scope = io_scope
        
    def __call__(self, iv_exprStr):
        
        lt_substrs = iv_exprStr.split()
        lv_symbol = lt_substrs[0]
        try:
            lt_args = lt_substrs[1:]
        except IndexError:
            lt_args = []
        lo_symbol = self.mo_scope.getSymbol(lv_symbol)
        if not callable(lo_symbol):
            rv_isTrue = lo_symbol
        else:
            rv_isTrue = self.mo_scope.getFuncSymbol(
                                                    iv_name = lv_symbol,
                                                    it_args = lt_args
                                                    )
        return rv_isTrue
            
class BoolExpr(object):
    
    def __init__(self,
                 iv_exprStr
                 ):
        self.mo_logExpr = BoolParser().parse(iv_exprStr)
        
    def is_true(self,
                io_scope
                ):
        
        return self.mo_logExpr.isTrue(_Evaluator(io_scope))
        
class IfBlock(CodeBlock):
    
    def __init__(self, io_ifexpr ):
        CodeBlock.__init__( self )
        self.mt_branches = []
        lt_components = self.mt_children[:]
        self.mt_branches.append( (io_ifexpr, lt_components) )
        
    def addComponent(self,
                     io_comp
                     ):
        CodeBlock.addComponent( self, io_comp )
        ls_branch = self.mt_branches[-1]
        ls_branch[1].append( io_comp )
        
    def addElif(self, io_expr):
        lo_new_child = CodeLines()
        self.mt_branches.append( ( io_expr, [] ) )
        self.addComponent( io_comp = lo_new_child )
            
    def addElse(self):
        lo_new_child = CodeLines()
        self.mt_branches.append( ( None, [] ) )
        self.addComponent( io_comp = lo_new_child )
                
    def addLine(self,
                iv_line
                ):
        ls_branch = self.mt_branches[-1]
        lo_child = ls_branch[1][-1]
        if not isinstance( lo_child, CodeLines ):
            lo_child = CodeLines()
            self.addComponent( io_comp = lo_child )
        lo_child.addLine( iv_line )
        
    def getCode(self,
                io_scope
                ):
        rt_codelines = []
        for ls_branch in self.mt_branches:
            lo_expr = ls_branch[0]    
            if lo_expr:
                if lo_expr.is_true( io_scope ):
                    lt_children = ls_branch[-1]
                    break
            else:
                lt_children = ls_branch[-1]
                break
        else:
            return rt_codelines
        
        for lo_child in lt_children:
            rt_codelines += lo_child.getCode( io_scope )
            
        return rt_codelines
        
class ForBlock(CodeBlock):
    
    def __init__(self, 
                 iv_table,
                 iv_rowname = "",
                 io_whereExpr = None
                 ):

        CodeBlock.__init__( self )
        
        self.mv_table = iv_table

        if iv_rowname:
            self.mv_rowname = iv_rowname
        else:
            self.mv_rowname = self.mv_table
        self.mo_where = io_whereExpr
        
    def getCode(self,
                io_scope
                ):
        
        rt_codelines = []
        
        if not isinstance(self.mv_table, list):
            lt_hlp = io_scope.getSymbol( self.mv_table )
        else:
            lv_func_name = self.mv_table[0]
            lt_args = self.mv_table[1:]
            lt_hlp = io_scope.getFuncSymbol(lv_func_name, lt_args)
        
        if self.mo_where is None:
            lt_table = lt_hlp
        else:
            lt_table = []
            lo_scope = ForScope(self.mv_rowname, lt_hlp)
            io_scope.addChild(lo_scope)
            for lv_idx, ls_row in enumerate(lt_hlp):
                lo_scope.setRow(lv_idx)
                if self.mo_where.is_true(lo_scope):
                    lt_table.append(ls_row)
        
        lo_scope = ForScope( self.mv_rowname, lt_table )
        
        io_scope.addChild( lo_scope )
        for lv_idx in range(0,len(lt_table)):
            lo_scope.setRow( lv_idx )
            rt_codelines += CodeBlock.getCode( self, lo_scope )
        return rt_codelines        
    
class UserComponent(CodeBlock):
    
    def __init__(self, inBlockName):
        
        CodeBlock.__init__(self)
        self._blockName = inBlockName
  
    def getCode(self,
                io_scope
                ):
        
        scope = io_scope
        userCode = scope.m_user_code
        while not userCode:
            if scope.mo_parent is None:
                raise NoUserCode
            scope = scope.mo_parent
            userCode = scope.m_user_code
        
        blockName = Translator(io_scope).translate(self._blockName)

        if userCode.isEmpty(blockName):
            defaultLines = CodeBlock.getCode(self, io_scope)
            userCode.setDefaultCode(blockName, defaultLines)
            
        return userCode(io_scope, blockName).split("\n")
      
