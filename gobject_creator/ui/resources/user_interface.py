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

from gobject_creator.ui.resources.util import get_resource_path

class UserInterface(object):
    
    def __init__(self, ui_file):
        
        self._builder = gtk.Builder()
        self._builder.set_translation_domain("goceditor")
        self._builder.add_from_file(get_resource_path(ui_file))
        
    def __del__(self):
        
        for obj in self._builder.get_objects():
            if isinstance(obj, gtk.Widget) and not obj.get_parent():
                obj.destroy()
                
    def __getattr__(self, name):
        
        if name != "_builder":
            return self.__dict__["_builder"].get_object(name)
        else:
            return self.__dict__[name]