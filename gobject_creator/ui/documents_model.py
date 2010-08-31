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

import gobject

class DocumentsModel(gobject.GObject):
    
    def __init__(self):
        
        gobject.GObject.__init__(self)
        
        self._documents = []
        self._emitting = False
                
    def new_document(self):
        
        idx = 0
        self._documents.insert(idx, _DocInfo(""))
        
        self._emitting = True
        self.emit("document-added", idx, "")
        self._emitting = False
        
    def load_document(self, file_path):
        
        for idx, info in enumerate(self._documents):
            if info.file_path == file_path:
                is_new = False
                info.state = DocState.SAVED
                break
        else:
            is_new = True
            idx = 0
            info = _DocInfo(file_path)
            info.state = DocState.SAVED
            self._documents.insert(idx, info)
            
        f = open(file_path, "r")
        content = f.read()
        f.close()
        
        self._emitting = True
        
        if is_new:
            self.emit("document-added", idx, content)
        else:
            self.emit("document-refreshed", idx, content)
            
        self._emitting = False
        
    def save_document(self, idx, file_path, content):
        
        f = open(file_path, "w")
        f.write(content)
        f.close()
        
        info = self._documents[idx]
        info.file_path = file_path
        info.state = DocState.SAVED
        
        self._emitting = True
        
        self.emit("document-changed", idx)

        self._emitting = False
        
    def touch_document(self, idx):
        
        if self._emitting:
            return
        
        if self._documents[idx].state != DocState.SAVED:
            return
        
        self._documents[idx].state = DocState.CHANGED
        
        self.emit("document-changed", idx)
        
    def close_document(self, idx):
        
        self._documents = self._documents[:idx] + \
            self._documents[idx+1:]
        
    def get_state(self, idx):
        
        return self._documents[idx].state
    
    def get_file_path(self, idx):
        
        return self._documents[idx].file_path
        
gobject.type_register(DocumentsModel)

gobject.signal_new(
    "document-added",
    DocumentsModel,
    gobject.SIGNAL_RUN_LAST,
    None,
    (gobject.TYPE_INT, 
     gobject.TYPE_STRING)
    )

gobject.signal_new(
    "document-refreshed",
    DocumentsModel,
    gobject.SIGNAL_RUN_LAST,
    None,
    (gobject.TYPE_INT, 
     gobject.TYPE_STRING)
    )

gobject.signal_new(
    "document-changed",
    DocumentsModel,
    gobject.SIGNAL_RUN_LAST,
    None,
    (gobject.TYPE_INT, )
    )

class DocState(object):
    
    NEW = 1
    CHANGED = 2
    SAVED = 3

class _DocInfo(object):
    
    def __init__(self, file_path):
        
        self.file_path = file_path
        self.state = DocState.NEW
