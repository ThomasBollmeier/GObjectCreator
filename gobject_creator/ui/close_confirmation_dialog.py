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

import gobject_creator
from ui.resources.user_interface import UserInterface

class CloseConfirmationDialog(UserInterface):
    
    SAVE = 1
    NO_SAVE = 2
    CANCEL = 3
    
    def __init__(self):
        
        UserInterface.__init__(self, "close_confirmation_dialog.ui")
        self.dialog.set_title("")
        
        self.dialog.connect("delete-event", self._on_delete)
        
    def run(self):
        
        self._result = 0
        
        response = self.dialog.run()
        
        if not self._result:
            if response == 1:
                self._result = CloseConfirmationDialog.NO_SAVE
            elif response == 2:
                self._result = CloseConfirmationDialog.CANCEL
            else:
                self._result = CloseConfirmationDialog.SAVE
        
        self.dialog.hide()
        
        return self._result
    
    def _on_delete(self, *args):
        
        self._result = CloseConfirmationDialog.CANCEL