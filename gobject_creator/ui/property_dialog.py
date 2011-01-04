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
from metamodel.meta_objects import *

class PropertyDialog(UserInterface):
    
    def __init__(self):
        
        UserInterface.__init__(self, "property_dialog.ui")
        
        self._init_prop_type_combo()
        self.property_type = PROP_STRING
        
        self._init_access_combo()
        self.access_type = PROP_ACCESS_READ
        
        self.create_attribute.connect("clicked", self._on_create_attr_clicked)
        self._on_create_attr_clicked(self.create_attribute)
                    
    def run(self):
        
        if self.property_dialog.run() == gtk.RESPONSE_OK:
            name = str(self.name.get_text())
            description = str(self.description.get_text())
            property_type = self.property_type
            gobject_type = str(self.gobject_type.get_text())
            access_type = self.access_type
            attr_name = str(self.attribute_name.get_text())
            res = (name, description, property_type, 
                   gobject_type, access_type, attr_name)
        else:
            res = ()
            
        self.property_dialog.hide()
        
        return res

    def _get_access_type(self):
        
        idx = self.access.get_active()
        if idx >= 0:
            return self._access_values[idx][1]
        else:
            return -1
        
    def _set_access_type(self, access):

        idx = 0
        for text, value in self._access_values:
            if value == access:
                self.access.set_active(idx)
                return
            else:
                idx += 1
                
    access_type = property(_get_access_type, _set_access_type)
    
    def _get_property_type(self):
        
        idx = self.prop_type.get_active()
        if idx >= 0:
            return self._prop_type_values[idx][1]
        else:
            return -1
        
    def _set_property_type(self, prop_type):

        idx = 0
        for text, value in self._prop_type_values:
            if value == prop_type:
                self.prop_type.set_active(idx)
                return
            else:
                idx += 1
                
    property_type = property(_get_property_type, _set_property_type)

    def _init_access_combo(self):
        
        text_renderer = gtk.CellRendererText()
        self.access.pack_start(text_renderer, True)
        self.access.add_attribute(text_renderer, "text", 0)
        
        self._access_values = []
        self._access_values.append((_("Read only"),PROP_ACCESS_READ))
        self._access_values.append(
            (_("Read/Initial Write"),PROP_ACCESS_CONSTRUCTOR)
        )
        self._access_values.append(
            (_("Read/Write"),PROP_ACCESS_READ_WRITE)
        )

        model = gtk.ListStore(gobject.TYPE_STRING)
        for text, value in self._access_values:
            model.append((text,))

        self.access.set_model(model)
    
    def _init_prop_type_combo(self):
        
        text_renderer = gtk.CellRendererText()
        self.prop_type.pack_start(text_renderer, True)
        self.prop_type.add_attribute(text_renderer, "text", 0)
        
        self._prop_type_values = []
        self._prop_type_values.append((_("Boolean"), PROP_BOOLEAN))
        self._prop_type_values.append((_("Integer"), PROP_INT))
        self._prop_type_values.append((_("Double"), PROP_DOUBLE))
        self._prop_type_values.append((_("String"), PROP_STRING))
        self._prop_type_values.append((_("Pointer"), PROP_POINTER))
        self._prop_type_values.append((_("Object"), PROP_OBJECT))
        self._prop_type_values.append((_("Enumeration"), PROP_ENUM))
        
        model = gtk.ListStore(gobject.TYPE_STRING)
        for text, value in self._prop_type_values:
            model.append((text,))

        self.prop_type.set_model(model)
        
        self.prop_type.connect("changed", self._on_prop_type_changed)
        
    def _on_prop_type_changed(self, combo):
        
        prop_type = self._get_property_type()
        
        if prop_type != PROP_OBJECT and prop_type != PROP_ENUM:
            self.gobject_type.set_text("")
            self.gobject_type.set_sensitive(False)
            self.label_gobject_type.set_sensitive(False)
            self.create_attribute.set_sensitive(True)
        else:
            self.gobject_type.set_sensitive(True)
            self.label_gobject_type.set_sensitive(True)
            self.create_attribute.set_active(False)
            self.create_attribute.set_sensitive(False)
                        
    def _on_create_attr_clicked(self, checkbutton, *args):
        
        create_attr = checkbutton.get_active()
        
        self.attribute_name.set_sensitive(create_attr)
        
        if create_attr:
            self.attribute_name.set_text(self.name.get_text())
        else:
            self.attribute_name.set_text("")
