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
from resources.user_interface import UserInterface
from metamodel.meta_objects import *

def run_method_dialog(is_intf_method = False):
    
    return MethodDialog(is_intf_method).run()

class MethodDialog(object):
    
    def __init__(self, is_intf_method):
        
        self._ui = UserInterface("method_dialog.ui")
        self._is_intf_method = is_intf_method

        self._ui.name.set_text("new_method")
        self._init_visi_combo()
    
        if not self._is_intf_method:
            self._ui.instance.set_active(True)
            self._ui.virtual.set_active(False)
            self._ui.abstract.set_active(False)
        else:
            self._ui.instance.set_active(True)
            self._ui.static.set_sensitive(False)
            self._ui.virtual.set_active(True)
            self._ui.virtual.set_sensitive(False)
            self._ui.abstract.set_active(True)
            self._ui.abstract.set_sensitive(False)
            
        self.set_visibility(PUBLIC)
        
        self._ui.virtual.connect("toggled",
                                 self._on_virtual_toggled
                                 )
        self._ui.abstract.connect("toggled",
                                  self._on_abstract_toggled
                                  )
            
    def run(self):
        
        dialog = self._ui.method_dialog
    
        if dialog.run() == gtk.RESPONSE_OK:
            name = str(self._ui.name.get_text())
            visi = self.get_visibility()
            if self._ui.instance.get_active():
                scope = INSTANCE
            else:
                scope = STATIC
            virtual = self._ui.virtual.get_active()
            abstract = self._ui.abstract.get_active()
            res = (name, visi, scope, virtual, abstract)
        else:
            res = ()
        
        return res
    
    def set_visibility(self, visi):
        
        if not self._is_intf_method:
            if visi == PUBLIC:
                self._ui.visibility.set_active(0)
            elif visi == PROTECTED:
                self._ui.visibility.set_active(1)
            elif visi == PRIVATE:
                self._ui.visibility.set_active(2)
        elif visi == PUBLIC:
            self._ui.visibility.set_active(0)
            
    def get_visibility(self):
        
        idx = self._ui.visibility.get_active()
        return [PUBLIC, PROTECTED, PRIVATE][idx]
            
    def _init_visi_combo(self):

        combo = self._ui.visibility
        
        text_renderer = gtk.CellRendererText()
        combo.pack_start(text_renderer, True)
        combo.add_attribute(text_renderer, "text", 0)
        
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)
        model.append((_("Public"), PUBLIC))
    
        if not self._is_intf_method:
            model.append((_("Protected"), PROTECTED))
            model.append((_("Private"), PRIVATE))

        combo.set_model(model)   
        
    def _on_virtual_toggled(self, button):
        
        if button.get_active():
            self._ui.instance.set_active(True)
            self._ui.static.set_sensitive(False)
        else:
            self._ui.static.set_sensitive(True)            
    
    def _on_abstract_toggled(self, button):
        
        if button.get_active():
            self._ui.virtual.set_active(True)
            self._ui.virtual.set_sensitive(False)
        else:
            self._ui.virtual.set_sensitive(True)
