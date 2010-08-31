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

from documents_view import DocumentsView
from documents_model import DocumentsModel
from resources.util import get_resource_path
import gobject_creator

class GOCEditor(object):
    """
    Simple editor that supports the creation of meta definition 
    files for GObjectCreator
    """
    
    def __init__(self):
        
        self._builder = gtk.Builder()
        
        path = get_resource_path("goceditor.ui")
        self._builder.add_from_file(path)
        
        self._create_widgets()
        
        self._builder.connect_signals(self)
        
    def run(self):
        
        window = self._builder.get_object("main_window")
        window.show_all()
        
        gtk.main()
           
    def on_file_new(self, *args):

        self._docs_model.new_document()
        
    def on_file_open(self, *args):
        
        dialog = gtk.FileChooserDialog(
            action = gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons = (_("Cancel"), gtk.RESPONSE_CANCEL,
                       _("Open"), gtk.RESPONSE_OK)
        )
        
        if dialog.run() == gtk.RESPONSE_OK:
            file_name = dialog.get_filename()
        else:
            file_name = None
        
        dialog.destroy()
        
        if file_name:
            self._docs_model.load_document(file_name)
            
    def on_file_save(self, *args):
        
        idx = self._documents.get_current_index()
        if idx < 0:
            return
        
        old_path = self._docs_model.get_file_path(idx)
        
        if os.path.exists(old_path):

            new_path = old_path

        else:
        
            dialog = gtk.FileChooserDialog(
                action = gtk.FILE_CHOOSER_ACTION_SAVE,
                buttons = (_("Cancel"), gtk.RESPONSE_CANCEL,
                           _("Save"), gtk.RESPONSE_OK)
            )
            
            dialog.set_current_name("new_file.goc")
            dialog.set_do_overwrite_confirmation(True)
        
            if dialog.run() == gtk.RESPONSE_OK:
                new_path = dialog.get_filename()
            else:
                new_path = None
                
            dialog.destroy()
                
        if new_path:
            content = self._documents.get_content(idx)
            self._docs_model.save_document(idx, new_path, content)
            
    def on_file_quit(self, *args):
        
        gtk.main_quit()
        
    def on_help_info(self, *args):
        
        builder = gtk.Builder()
        builder.add_from_file(get_resource_path("gocedit_info.ui"))
        
        dialog = builder.get_object("info_dialog")
        
        path = get_resource_path("hand_mit_stift_296x300.png")
        logo = gtk.gdk.pixbuf_new_from_file(path)
        dialog.set_logo(logo)
        
        dialog.set_version(gobject_creator.VERSION)
        
        dialog.run()
        dialog.destroy()
                
    def _create_widgets(self):
        
        self._docs_model = DocumentsModel()
        self._documents = DocumentsView(self._docs_model)
        self._documents.widget.show()
        
        vbox = self._builder.get_object("top_vbox")
        vbox.show()
        vbox.pack_start(self._documents.widget)
                
if __name__ == "__main__":
    
    editor = GOCEditor()
    editor.run()
        