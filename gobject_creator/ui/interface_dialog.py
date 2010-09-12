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

import pygtk
pygtk.require("2.0")
import gtk

from ui.resources.user_interface import UserInterface

class InterfaceDialog(object):
   
    def __init__(self):
        
        self._ui = UserInterface("interface_dialog.ui")
    
    def run(self):
        
        dialog = self._ui.interface_dialog
        
        if dialog.run() == gtk.RESPONSE_OK:
            name = str(self._ui.name.get_text())
            prefix = str(self._ui.prefix.get_text())
            res = (name, prefix)
        else:
            res = ()
            
        dialog.destroy()
        
        return res