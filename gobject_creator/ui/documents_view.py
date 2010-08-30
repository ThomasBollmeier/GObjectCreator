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
from gtksourceview2 import \
     View, Buffer, Language, LanguageManager

import code_creation
from resources.util import get_resource_path

class DocumentsView(object):
    
    def __init__(self):
        
        self._language_manager = LanguageManager()
        language_path = os.path.dirname(__file__)
        language_path = os.path.abspath(language_path)
        language_path += os.sep + "resources"
        search_path = self._language_manager.get_search_path()
        search_path.insert(0, language_path)
        self._language_manager.set_search_path(search_path)
        
        self._notebook = gtk.Notebook()
        self._notebook.set_property("scrollable", True)
        
        self._popup = None
        self._create_popup_menu()
        
        self._documents = []
        self._doc_handlers = {}
        self._num_new_docs = 0
        
    def add_document(self, file_name=""):
        
        if file_name:
            view = self._get_document_view(file_name)
        else:
            view = None

        new_doc = view is None
        
        text = ""
        if file_name:
            try:
                f = open(file_name, "r")
                text = f.read()
                f.close()
            except IOError:
                pass #todo: Fehlermeldung
        else:
            file_name = self._new_file_name()
        
        if new_doc:
            
            view = View()
            view.show()
    
            lang = self._language_manager.get_language("gobject-creator")
            buf = Buffer(language=lang)
            buf.set_highlight_syntax(True)
            view.set_buffer(buf)
        
            doc_container = gtk.ScrolledWindow()
            doc_container.show()
            doc_container.add(view)
            
            hbox = gtk.HBox()
            hbox.show()
            
            label = gtk.Label(os.path.basename(file_name))
            label.show()
            hbox.pack_start(label)
            
            close_button = gtk.Button()
            image = gtk.Image()
            image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
            close_button.set_image(image)
            close_button.set_relief(gtk.RELIEF_NONE)
            close_button.show()
            hbox.pack_start(close_button)
    
            self._notebook.prepend_page(doc_container,
                                        hbox
                                        )
            self._notebook.set_current_page(0)
            
            self._documents.insert(0, file_name)
            
        else:
            # existierendes Dokument
            idx = self._documents.index(file_name)
            self._notebook.set_current_page(idx)

        if text:
            view.get_buffer().set_text(text)

        if new_doc:
            # Event handling:
            view.connect("button_press_event",
                         self._on_button_pressed
                         )
            
            handler_info = _DocumentHandlerInfo()
            
            handler_info.close_handler_id = close_button.connect(
                "clicked", 
                self._on_document_closed, 
                file_name
            )
      
            buf = view.get_buffer()
            handler_info.change_handler_id = buf.connect(
                "changed",
                self._on_document_changed,
                file_name
            )
            
            self._doc_handlers[file_name] = handler_info
            
    def get_current_file_path(self):
        
        idx = self._notebook.get_current_page()
        if idx >= 0:
            return self._documents[idx]
        else:
            return None
        
    def get_content(self, path):
        
        idx = self._documents.index(path)
        view = self._notebook.get_nth_page(idx).get_child()
        buf = view.get_buffer()
        
        return buf.get_text(buf.get_start_iter(),
                            buf.get_end_iter()
                            )
        
    def set_file_path_after_save(self, old_path, new_path):
        
        try:
            if old_path != new_path:
                idx = self._documents.index(old_path)
                self._reconnect_handlers(
                    idx, 
                    old_path, 
                    new_path
                    )
                self._documents[idx] = new_path
            self._set_document_title(new_path, False)
        except:
            pass
        
    def _reconnect_handlers(self, 
                            doc_idx, 
                            old_path, 
                            new_path
                            ):
         
        page = self._notebook.get_nth_page(doc_idx)

        buf = page.get_child().get_buffer()
        
        hbox = self._notebook.get_tab_label(page)
        close_button = hbox.get_children()[1]
        
        handler_info = self._doc_handlers[old_path]
        buf.disconnect(handler_info.change_handler_id)
        close_button.disconnect(handler_info.close_handler_id)
        
        del self._doc_handlers[old_path]
        
        handler_info.close_handler_id = close_button.connect(
            "clicked", 
            self._on_document_closed, 
            new_path
        )
  
        handler_info.change_handler_id = buf.connect(
            "changed",
            self._on_document_changed,
            new_path
        )
        
        self._doc_handlers[new_path] = handler_info
                
    def _create_popup_menu(self):
        
        if not self._popup:
            
            self._actions = gtk.ActionGroup("EditorActions")
            self._add_action("package-new", _("New Package"))
            self._add_action("class", _("Class"))
            self._add_action("class-new", _("New"))
            self._add_action("class-implements", _("Implements..."))
            self._add_action("class-constructor", _("Constructor"))
            self._add_action("class-constructor-new", _("New"))
            self._add_action("class-constructor-param", _("New Parameter"))
            self._add_action("class-constructor-initprop", _("New Property Init."))
            self._add_action("class-method", _("Method"))
            self._add_action("class-method-new", _("New"))
            self._add_action("class-method-result", _("New Result"))
            self._add_action("class-method-param", _("New Parameter"))
            self._add_action("class-override", _("Override..."))
            self._add_action("class-attr", _("New Attribute"))
            self._add_action("class-prop", _("New Property"))
            self._add_action("class-signal", _("Signal"))
            self._add_action("class-signal-new", _("New"))
            self._add_action("class-signal-param", _("New Parameter"))
            self._add_action("interface", _("Interface"))
            self._add_action("interface-new", _("New"))
            self._add_action("interface-extends", _("Extends..."))
            self._add_action("interface-method", _("Method"))
            self._add_action("interface-method-new", _("New"))
            self._add_action("interface-method-result", _("New Result"))
            self._add_action("interface-method-param", _("New Parameter"))
            self._add_action("interface-signal", _("Signal"))
            self._add_action("interface-signal-new", _("New"))
            self._add_action("interface-signal-param", _("New Parameter"))
             
            mngr = gtk.UIManager()
            mngr.insert_action_group(self._actions)
            mngr.add_ui_from_file(
                self._get_resource_path("popup_menu.xml"))
            self._popup = mngr.get_widget("/ui/popup")
            
            # Codesnippet callbacks
            self._codesnippet = {}
            self._codesnippet["package-new"] = \
                code_creation.codesnippet_package
            self._codesnippet["class-new"] = \
                code_creation.codesnippet_class
            self._codesnippet["class-implements"] = \
                code_creation.codesnippet_implements
            self._codesnippet["class-constructor-new"] = \
                code_creation.codesnippet_constructor
            self._codesnippet["class-constructor-param"] = \
                code_creation.codesnippet_constructor_param
            self._codesnippet["class-constructor-initprop"] = \
                code_creation.codesnippet_init_property
            self._codesnippet["class-method-new"] = \
                code_creation.codesnippet_method
            self._codesnippet["class-method-result"] = \
                code_creation.codesnippet_result
            self._codesnippet["class-method-param"] = \
                code_creation.codesnippet_param
            self._codesnippet["class-override"] = \
                code_creation.codesnippet_override
            self._codesnippet["class-attr"] = \
                code_creation.codesnippet_attr
            self._codesnippet["class-prop"] = \
                code_creation.codesnippet_property
            self._codesnippet["class-signal-new"] = \
                code_creation.codesnippet_signal
            self._codesnippet["class-signal-param"] = \
                code_creation.codesnippet_param
            self._codesnippet["interface-new"] = \
                code_creation.codesnippet_interface
            self._codesnippet["interface-method-new"] = \
                code_creation.codesnippet_intf_method
            self._codesnippet["interface-method-result"] = \
                code_creation.codesnippet_result
            self._codesnippet["interface-method-param"] = \
                code_creation.codesnippet_param
            self._codesnippet["interface-signal-new"] = \
                code_creation.codesnippet_signal
            self._codesnippet["interface-signal-param"] = \
                code_creation.codesnippet_param
            
        return self._popup

    def _add_action(self, name, label):
        
        action = gtk.Action(name, label, name, None)
        action.connect("activate", self._on_popup_action_activated)
        self._actions.add_action(action)
    
    def _get_document_view(self, file_name):
        
        try:
            idx = self._documents.index(file_name)
            return self._notebook.get_nth_page(idx).get_child()
        except ValueError:
            return None

    def _get_line_begin_at_cursor_pos(self):
        
        page_idx = self._notebook.get_current_page()
        doc_view = self._notebook.get_nth_page(page_idx).get_child()
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

    def _get_resource_path(self, file_name):
               
        return get_resource_path(file_name)
    
    def _get_widget(self):
        
        return self._notebook
    
    widget = property(_get_widget)
    
    def _new_file_name(self):
        
        file_name = _("Untitled")
        
        if self._num_new_docs:
            file_name += "%d" % self._num_new_docs
        
        self._num_new_docs += 1
        
        return file_name
    
    def _set_document_title(self, file_name, doc_changed=True):
        
        idx = self._documents.index(file_name)
        page = self._notebook.get_nth_page(idx)
        hbox = self._notebook.get_tab_label(page)
        label = hbox.get_children()[0]
        text = os.path.basename(file_name)
        if doc_changed:
            text += "*"
        label.set_text(text)
            
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
    
    def _on_document_changed(self, buffer, file_name):

        self._set_document_title(file_name)
        
    def _on_popup_action_activated(self, action, *args):
        
        name = action.get_name()
        
        if name in self._codesnippet:
            
            line_begin = self._get_line_begin_at_cursor_pos()
            code = self._codesnippet[name](line_begin)
            
            if code:
                page_idx = self._notebook.get_current_page()
                doc_container = self._notebook.get_nth_page(page_idx)
                doc_view = doc_container.get_child()
                buf = doc_view.get_buffer()
                buf.insert_at_cursor(u"%s" % code)

        else:
            pass
    
    def _on_document_closed(self, button, file_name):
        
        page_idx = self._documents.index(file_name)
        if page_idx >= 0:
            self._notebook.remove_page(page_idx)
            self._documents.remove(file_name)
            del self._doc_handlers[file_name]
            
class _DocumentHandlerInfo(object):
    
    def __init__(self):
        
        self.close_handler_id = None
        self.change_handler_id = None