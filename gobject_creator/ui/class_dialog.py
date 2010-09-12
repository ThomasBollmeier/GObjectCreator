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

from resources.user_interface import UserInterface

def run_class_dialog():
    
    ui = UserInterface("class_dialog.ui")
    
    if ui.class_dialog.run() == gtk.RESPONSE_OK:
        name = ui.name.get_text()
        super_class = ui.super_class.get_text()
        abstract = ui.abstract.get_active()
        prefix = ui.prefix.get_text()
        result = (name, super_class, abstract, prefix)
    else:
        result = ()
        
    ui.class_dialog.destroy()
    
    return result
    