# coding=UTF-8

from classmate.code_generation.scope import Scope
import re

class Translator(object):
    
    """Hilfsklasse zur Codegenerierung aus Schablonen"""
    
    _go_func = re.compile( r"(.+?)\((.*)\)" )
    _SYMBOL = "\$" 
    
    def __init__(self,
                 io_scope
                 ):
        self.__mo_scope = io_scope
        self.__mth_symRe = {}

    @staticmethod
    def set_symbol_delimiter( in_delim="\$" ):
        Translator._SYMBOL = in_delim
        
    def translate(self,
                  iv_line
                  ):
        """ Quelltext durch Ersetzung von Symbolen erzeugen"""
        self.__mv_nested = 0
        return self.__replaceSymbols( iv_line )
    
    def __createRegex( self ):
        lv_number = self.__mv_nested + 1
        lv_hlp = r"(?<!%(sym)s)%(sym)s{%%s}(?!%(sym)s)" % \
        {"sym" : Translator._SYMBOL }
        lv_hlp = lv_hlp % lv_number
        lv_raw = r"%s(.+?)%s" % ( lv_hlp, lv_hlp )
        return re.compile( lv_raw )
    
    def __getRegex( self ):
        try:
            ro_regex = self.__mth_symRe[self.__mv_nested]
        except KeyError:
            ro_regex = self.__createRegex()
            self.__mth_symRe[self.__mv_nested] = ro_regex
        return ro_regex
        
    def __replaceSymbols( self, 
                          iv_line 
                          ):
        rv_line = iv_line[:]
        lo_regex = self.__getRegex()
        self.__mv_nested += 1
        rv_line = lo_regex.sub( self.__replaceSymbol, rv_line )
        self.__mv_nested -= 1
        return rv_line

    def __replaceSymbol( self,
                         io_match 
                         ):
        lv_symbol = io_match.group( 1 )
        lo_match = Translator._go_func.search( lv_symbol )
        if not lo_match:
            rv_value = self.__mo_scope.getSymbolStr( lv_symbol )
        else:
            lv_funcname = lo_match.group(1)
            lv_args = self.__replaceSymbols( lo_match.group(2) )
            lt_args = [ lv_arg.strip()
                       for lv_arg in lv_args.split(",")
                       if lv_arg
                       ]
            rv_value = self.__mo_scope.getFuncSymbol( lv_funcname, lt_args )
        return rv_value
    
if __name__ == "__main__":
    
    def lower(io_scope,iv_string):
        return iv_string.lower()
    
    go_scope = Scope()
    go_scope.addSymbol( "class", "Person" )
    go_scope.addSymbol( "lower", lower )
    
    Translator.set_symbol_delimiter( "@" )
    gv_line = "class C@lower( @@class@@ )@: pass"
        
    print Translator(go_scope).translate( gv_line )
    
