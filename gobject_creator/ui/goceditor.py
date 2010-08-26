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
<http://www.gnu.
"""

import os

import pygtk
pygtk.require("2.0")
import gtk

from documents_view import DocumentsView

class GOCEditor(object):
    """
    Simple editor that supports the creation of meta definition 
    files for GObjectCreator
    """
    
    def __init__(self):
        
        path = os.path.abspath(os.path.dirname(__file__))
        path += os.sep + "resources" + os.sep + "goceditor.ui"
        
        self._builder = gtk.Builder()
        self._builder.add_from_file(path)
        
        self._create_widgets()
        
        self._builder.connect_signals(self)
        
    def run(self):
        
        window = self._builder.get_object("main_window")
        window.show_all()
        
        gtk.main()
           
    def on_file_new(self, *args):

        self._documents.add_document()
        
    def on_file_quit(self, *args):
        
        gtk.main_quit()
        
    def _create_widgets(self):
        
        self._documents = DocumentsView()
        self._documents.widget.show()
        
        hpanes = self._builder.get_object("horizontal_panes")
        hpanes.show()
        hpanes.add2(self._documents.widget)
        
        
if __name__ == "__main__":
    
    editor = GOCEditor()
    editor.run()
        