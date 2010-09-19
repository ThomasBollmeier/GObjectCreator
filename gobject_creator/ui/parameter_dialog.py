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

import os.path
import gettext
_ = gettext.gettext 

import pygtk
pygtk.require("2.0")
import gtk
import gobject

import gobject_creator
from ui.resources.user_interface import UserInterface
from ui.code_view import CodeView
from metamodel.meta_objects import *
from metamodel.introspection_info import ParamCategory

class ParameterData(object):
    
    def __init__(self,
                 name,
                 type_name,
                 is_constant
                 ):
        
        self.name = name
        self.type_name = type_name
        if is_constant:
            self.type_name = "const " + self.type_name
            
        self.intro = _IntrospectionData()

class ParameterDialog(UserInterface):
    
    def __init__(self, 
                 result_dialog = False
                 ):
        
        UserInterface.__init__(self, "parameter_dialog.ui")
        
        if not result_dialog:
            self.label_name.show()
            self.name.show()
        else:
            self.label_name.hide()
            self.name.hide()
        
        self._param_catg = CodeView(self.param_catg)
        if not result_dialog:
            self._param_catg.add_value(" --- ", None)
            self._param_catg.add_value(_("Input"), ParamCategory.IN)
            self._param_catg.add_value(_("Output"), ParamCategory.OUT)
            self._param_catg.add_value(_("Input/Output"), ParamCategory.INOUT)
            self._param_catg.add_value(_("UserData"), ParamCategory.USER_DATA)
        else:
            self._param_catg.add_value(_("Result"), ParamCategory.RESULT)
            self._param_catg.set_value(ParamCategory.RESULT)
        
        self._transfer_mode = CodeView(self.transfer_mode)
        self._transfer_mode.add_value(" --- ", "UNSPECIFIED")
        self._transfer_mode.add_value(_("No Transfer"), "NONE")
        self._transfer_mode.add_value(_("Transfer Container"), 
                                      "CONTAINER_ONLY")
        self._transfer_mode.add_value(_("Transfer Full"), "FULL")
        
        self._data_catg = CodeView(self.data_catg)
        self._data_catg.add_value(_("Elementary"), _DataCatg.ELEMENTARY)
        self._data_catg.add_value(_("List"), _DataCatg.LIST)
        self._data_catg.add_value(_("Dictionary"), _DataCatg.DICTIONARY)
                
        self._data_type = self._data_type_code_view_new(self.data_type)
        
        self._element_type = self._data_type_code_view_new(self.element_type)
        
        self._key_type = self._data_type_code_view_new(self.key_type)
        self._value_type = self._data_type_code_view_new(self.value_type)
        
        self.radio_fixed_length.connect("toggled",
                                        self._on_radio_length_toggled
                                        )
        self.radio_from_param.connect("toggled",
                                      self._on_radio_length_toggled
                                      )
        self.data_catg.connect("changed", 
                               self._on_data_catg_changed,
                               self._data_catg
                               )

        self._on_radio_length_toggled(self.radio_fixed_length)
        self._on_data_catg_changed(self.data_catg, 
                                   self._data_catg
                                   )
        
    def run(self):
        
        if self.parameter_dialog.run() == gtk.RESPONSE_OK:
            name = str(self.name.get_text())
            type_name = str(self.param_type.get_text())
            is_constant = self.const.get_active()
            res = ParameterData(name, 
                                type_name, 
                                is_constant
                                )
            res.intro = self._get_introspection_data()
        else:
            res = None
        
        self.parameter_dialog.hide()
        
        return res
    
    def _get_introspection_data(self):
        
        res = _IntrospectionData()
        
        res.param_catg = self._param_catg.get_value()
        res.transfer_mode = self._transfer_mode.get_value()
        res.description = str(self.description.get_text())
        
        res.data_catg = self._data_catg.get_value()

        if res.data_catg == _DataCatg.ELEMENTARY:
            res.data_type = self._data_type.get_value()
        elif res.data_catg == _DataCatg.LIST:
            res.elem_type = self._element_type.get_value()
            res.fixed_length = self.fixed_length.get_value_as_int()
            res.length_from_param = str(self.length_param.get_text())
            res.zero_terminated = self.zero_terminated.get_active()
        elif res.data_catg == _DataCatg.DICTIONARY:
            res.key_type = self._key_type.get_value()
            res.value_type = self._value_type.get_value()
                
        return res
    
    def _data_type_code_view_new(self, 
                                 combo,
                                 allow_unspecified=True):
        
        res = CodeView(combo)
        if allow_unspecified:
            res.add_value(" --- ", "UNSPECIFIED")
        res.add_value("any", "POINTER")
        res.add_value("boolean", "BOOLEAN")
        res.add_value("int", "INTEGER")
        res.add_value("float", "FLOAT")
        res.add_value("double", "DOUBLE")
        res.add_value("utf8", "STRING")
        res.add_value("GType", "GTYPE")
        res.add_value("Object", "GOBJECT")
        res.add_value("size_t", "SIZE_T")
        res.add_value("filename", "FILENAME")
        
        return res

    def _on_data_catg_changed(self, combo, code_view):
        
        data_catg = code_view.get_value()
        
        is_elem = data_catg == _DataCatg.ELEMENTARY
        is_list = data_catg == _DataCatg.LIST
        is_dict = data_catg == _DataCatg.DICTIONARY
        
        self.data_type.set_sensitive(is_elem)
        self._data_type.set_value("UNSPECIFIED")
        
        self.element_type.set_sensitive(is_list)
        self._element_type.set_value("UNSPECIFIED")
        self.radio_fixed_length.set_sensitive(is_list)
        self.radio_from_param.set_sensitive(is_list)
        self.zero_terminated.set_sensitive(is_list)
        self.zero_terminated.set_active(False)
        self.fixed_length.set_sensitive(is_list)
        self.fixed_length.set_value(0)
        self.length_param.set_sensitive(False)
        self.length_param.set_text("")
        if is_list:
            self.radio_fixed_length.set_active(True)
            
        self.key_type.set_sensitive(is_dict)
        self._key_type.set_value("UNSPECIFIED")
        self.value_type.set_sensitive(is_dict)
        self._value_type.set_value("UNSPECIFIED")
        
    def _on_radio_length_toggled(self, radio):
        
        if not radio.get_active():
            return
        
        self.fixed_length.set_sensitive(False)
        self.fixed_length.set_value(0)
        self.length_param.set_sensitive(False)
        self.length_param.set_text("")
        
        if radio is self.radio_fixed_length:
            self.fixed_length.set_sensitive(True)
        elif radio is self.radio_from_param:
            self.length_param.set_sensitive(True)
        
class _DataCatg:
    
    ELEMENTARY = 1
    LIST = 2
    DICTIONARY = 3
    
DataCatg = _DataCatg

class _IntrospectionData(object):
    
    def __init__(self):
        
        self.param_catg = None
        self.transfer_mode = "UNSPECIFIED"
        self.description = ""
        self.data_catg = None
        self.data_type = "UNSPECIFIED"
        self.elem_type = "UNSPECIFIED"
        self.fixed_length = 0
        self.length_from_param = ""
        self.zero_terminated = False
        self.key_type = "UNSPECIFIED"
        self.value_type = "UNSPECIFIED"
        
        
        