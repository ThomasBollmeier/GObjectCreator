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
import gettext
_ = gettext.gettext
import locale

import pygtk
pygtk.require("2.0")
import gtk
import gobject

class CodeView(object):
    
    def __init__(self, combo):
        
        self._combo = combo
        
        text_renderer = gtk.CellRendererText()
        combo.pack_start(text_renderer, True)
        combo.add_attribute(text_renderer, "text", 0)        
        
        self._model = gtk.ListStore(gobject.TYPE_STRING)
        self._combo.set_model(self._model)

        self._labels_values = []
        
    def add_value(self, label, value):
        
        self._labels_values.append((label, value))
        self._model.append((label,))
        
    def get_value(self):
        
        idx = self._combo.get_active()
        if idx >= 0:
            return self._labels_values[idx][1]
        else:
            return None
        
    def set_value(self, value):
        
        idx = 0
        for label, val in self._labels_values:
            if val == value:
                self._combo.set_active(idx)
                return
            idx += 1
            
    def _get_combo_box(self):
        
        return self._combo
    
    combo_box = property(_get_combo_box)
    