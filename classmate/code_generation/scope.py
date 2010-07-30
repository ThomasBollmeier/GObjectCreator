# coding=UTF-8

gc_comp_separator = "."

class Scope:
    """
    Eine Instanz von Scope definiert einen Gueltigkeitsbereich von
    Symbolen in einer Quelltextschablone. Gueltigkeitsbereiche koennen
    ineinander verschachtelt werden (--> Methode "addChild" ).
    """

    def __init__( self ):
        self.mo_parent = None
        self.mth_symbols = {}
        self.m_user_code = None
        self.addSymbol("user_code", self._user_code)
                
    def addChild(self,
                 io_scope
                 ):
        io_scope.mo_parent = self

    def addSymbol( self,
                   iv_name,
                   iv_value
                   ):
        self.mth_symbols[iv_name] = iv_value

    def __setitem__( self,
                     iv_name,
                     iv_value
                     ):
        if not type( iv_name ) == str:
            raise TypeError
        self.addSymbol( iv_name, iv_value )
        
    def getSymbolStr( self,
                      iv_name
                      ):
        return str( self.getSymbol( iv_name ) )

    def getSymbol( self,
                   iv_name
                   ):
        
        lt_comps = iv_name.split( gc_comp_separator )
        lo_scope = self
        rv_value = None
        
        while lo_scope and rv_value == None:
            lv_len = len( lt_comps )
            while lv_len > 0:
                lv_name = gc_comp_separator.join( lt_comps[:lv_len] )
                try:
                    rv_value = lo_scope.mth_symbols[lv_name]
                    break # --> gefunden
                except KeyError:
                    rv_value = None
                    lv_len -= 1
            else:
                # --> nicht gefunden => mit äußerem Scope erneut versuchen:
                lo_scope = lo_scope.mo_parent
                
        if rv_value == None:
            raise UnknownSymbol, iv_name
        
        if lv_len < len( lt_comps ):
            for lv_comp in lt_comps[lv_len:]:
                rv_value = getattr( rv_value, lv_comp )

        return rv_value

    def getFuncSymbol( self,
                       iv_name,
                       it_args
                       ):
        lo_func = self.getSymbol( iv_name )
        # Scope ist immer erstes Argument:
        lt_args = [self] + it_args
        
        return lo_func( *lt_args )
    
    def set_user_code(self, in_user_code):
        
        self.m_user_code = in_user_code
    
    def _user_code(self,
                   in_scope,
                   in_blockname
                   ):
        
        scope = in_scope
        while scope and not scope.m_user_code:
            scope = scope.mo_parent
        if scope:
            return scope.m_user_code(in_scope, in_blockname)
        else:
            return ""
    
class ForScope(Scope):
    
    def __init__(self,
                 iv_table,
                 it_rows
                 ):
        Scope.__init__( self )
        self.mv_row = iv_table
        self.mt_rows = it_rows
        
    def setRow(self, 
               iv_index 
               ):
        self.mv_index = iv_index
        self.ms_row = self.mt_rows[self.mv_index]
        self.addSymbol( self.mv_row, self.ms_row )
    
    def getIndex(self):
        return self.mv_index
    
    def getMaxIndex(self):
        return len(self.mt_rows) - 1
    
class UnknownSymbol(Exception):
    pass

