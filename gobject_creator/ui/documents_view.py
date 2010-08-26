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

import os.path
import gettext
_ = gettext.gettext 

import pygtk
pygtk.require("2.0")
import gtk
from gtksourceview2 import View

import code_creation

class DocumentsView(object):
    
    class PopupItem:
        
        PACKAGE = "package"
        CLASS = "class"
        INTERFACE = "interface"
    
    def __init__(self):
        
        self._notebook = gtk.Notebook()
        self._notebook.set_property("scrollable", True)
        
        self._documents = []
        self._num_new_docs = 0
        
    def add_document(self, file_name=""):
        
        if not file_name:
            file_name = self._new_file_name()
        
        view = View()
        view.show()
        
        hbox = gtk.HBox()
        hbox.show()
        
        label = gtk.Label(file_name)
        label.show()
        hbox.pack_start(label)
        
        close_button = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close_button.set_image(image)
        close_button.set_relief(gtk.RELIEF_NONE)
        close_button.show()
        hbox.pack_start(close_button)
        
        # Event handling:
        
        view.connect("button_press_event",
                     self._on_button_pressed
                     )
        
        close_button.connect("clicked", 
                             self._on_document_closed, 
                             file_name
                             )
                
        self._notebook.prepend_page(view,
                                    hbox
                                    )
        
        self._documents.insert(0, file_name)
        
    def _create_popup_menu(self):
        
        menu = gtk.Menu()
        
        item = gtk.MenuItem(_("New Package"))
        item.show()
        menu.append(item)
        item.connect("activate", 
                     self._on_popup_selected, 
                     self.PopupItem.PACKAGE
                     )

        item = gtk.MenuItem(_("New Class"))
        item.show()
        menu.append(item)
        item.connect("activate", 
                     self._on_popup_selected, 
                     self.PopupItem.CLASS
                     )

        item = gtk.MenuItem(_("New Interface"))
        item.show()
        menu.append(item)
        item.connect("activate", 
                     self._on_popup_selected, 
                     self.PopupItem.INTERFACE
                     )
        
        return menu

    def _get_line_start_at_cursor_pos(self):
        
        page_idx = self._notebook.get_current_page()
        doc_view = self._notebook.get_nth_page(page_idx)
        buf = doc_view.get_buffer()
       
        end = buf.get_iter_at_mark(buf.get_insert())
        line_idx = end.get_line()
        start = buf.get_iter_at_line(line_idx)
        
        line_begin = ""
        tmp = buf.get_text(start, end)
        for ch in tmp:
            if ch != "\t":
                line_begin += " "
            else:
                line_begin += ch
        
        return line_begin

    def _get_widget(self):
        
        return self._notebook
    
    widget = property(_get_widget)
    
    def _new_file_name(self):
        
        file_name = _("Untitled")
        
        if self._num_new_docs:
            file_name += "%d" % self._num_new_docs
        
        self._num_new_docs += 1
        
        return file_name
    
    def _on_button_pressed(self, view, event):
        
        if event.type != gtk.gdk.BUTTON_PRESS:
            return False
        
        if event.button == 3:
            menu = self._create_popup_menu()
            menu.popup(None, None, None, 
                       event.button, event.get_time())
        else:
            return False
        
        return True # stop further handling
    
    def _on_popup_selected(self, item, name):
        
        line_begin = self._get_line_start_at_cursor_pos()
        
        try:
            code = self._codesnippet[name](line_begin)
        except KeyError:
            return
        except AttributeError:
            self._codesnippet = {}
            self._codesnippet[self.PopupItem.PACKAGE] = \
                code_creation.codesnippet_package
            self._codesnippet[self.PopupItem.CLASS] = \
                code_creation.codesnippet_class
            self._codesnippet[self.PopupItem.INTERFACE] = \
                code_creation.codesnippet_interface
            try:
                code = self._codesnippet[name](line_begin)
            except KeyError:
                return
            
        page_idx = self._notebook.get_current_page()
        document_view = self._notebook.get_nth_page(page_idx)
        buf = document_view.get_buffer()
        buf.insert_at_cursor(u"%s" % code)
    
    def _on_document_closed(self, button, file_name):
        
        page_idx = self._documents.index(file_name)
        if page_idx >= 0:
            self._notebook.remove_page(page_idx)
            self._documents.remove(file_name)