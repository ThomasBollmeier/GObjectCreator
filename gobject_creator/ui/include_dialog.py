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
import gtk

from gobject_creator.ui.resources.user_interface import UserInterface

class IncludeDialog(UserInterface):
    
    def __init__(self):
        
        UserInterface.__init__(self, "include_dialog.ui")
        
        self.browse_button.connect("clicked", self._on_browse_button_clicked)
        
    def run(self):
        
        if self.dialog.run() == gtk.RESPONSE_OK:
            res = str(self.model_file.get_text())
        else:
            res = None
            
        self.dialog.hide()
        
        return res
    
    def _on_browse_button_clicked(self, button):
        
        dialog = gtk.FileChooserDialog(
                                       title=_("Choose Model File"),
                                       action = gtk.FILE_CHOOSER_ACTION_OPEN,
                                       buttons = (
                                                  gtk.STOCK_CANCEL,
                                                  gtk.RESPONSE_CANCEL,
                                                  gtk.STOCK_OPEN,
                                                  gtk.RESPONSE_OK
                                                  )
                                       )
        
        if dialog.run() == gtk.RESPONSE_OK:
            model_file = os.path.basename(dialog.get_filename())
            self.model_file.set_text(model_file)
            
        dialog.destroy()
        
        