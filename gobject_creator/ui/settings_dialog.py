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
import gobject
import gconf

import gobject_creator
from ui.resources.user_interface import UserInterface
from metamodel.meta_objects import *

class Settings(gobject.GObject):
    
    _single = None
    
    @staticmethod
    def get():
        
        if not Settings._single:
            Settings._single = Settings() 
            
        return Settings._single
            
    def __init__(self):
        
        gobject.GObject.__init__(self)
        
        self._config_dir = "/apps/goceditor"
        
        self._config = gconf.client_get_default()
        self._config.add_dir(self._config_dir,
                             gconf.CLIENT_PRELOAD_NONE
                             )
        self._config.notify_add(self._config_dir,
                                self._on_config_changed
                                )
                
        self._options = {
                         "show_line_numbers" : gconf.VALUE_BOOL
                         }
        
        self._update_config = False
        
        for opt_name in self._options:
            setattr(self, opt_name, self._get_conf_value(opt_name))
            
        self._update_config = True
                       
    def _on_config_changed(self,
                           client,
                           connection_id,
                           entry,
                           *args
                           ):
        
        opt_name = entry.key.split("/")[-1]
        
        if self._options[opt_name] == gconf.VALUE_BOOL:
            opt_value = entry.value.get_bool()
        else:
            opt_value = None
            
        if opt_value is not None:
            self._update_config = False
            setattr(self, opt_name, opt_value)
            self._update_config = True
                
    def _get_conf_value(self, name):
        
        conf_key = self._config_dir + "/" + name
        value_type = self._options[name]
        
        value = self._config.get(conf_key)
        
        if value:
            if value.type == value_type:
                return value.get_bool()
            else:
                raise SettingsError
        else:
            if value_type == gconf.VALUE_BOOL:
                return False
            else:
                raise SettingsError
                    
    def _set_conf_value(self, name, value):
        
        conf_key = self._config_dir + "/" + name
        if type(value) == bool:
            self._config.set_bool(conf_key, value)
        
    def __setattr__(self, name, value):
        
        try:
            old_value = self.__dict__[name]
            is_different = old_value != value
        except KeyError:
            is_different = True    
            
        if is_different:
            self.__dict__[name] = value
            try:
                options = self.__dict__["_options"]
            except KeyError:
                options = {}
            if name in options:
                if self._update_config:
                    self._set_conf_value(name, value)
                self.emit("settings-changed", name)
            
gobject.type_register(Settings)

gobject.signal_new(
    "settings-changed",
    Settings,
    gobject.SIGNAL_RUN_LAST,
    None,
    (gobject.TYPE_STRING,)
    )

class SettingsError(Exception):
    
    pass
        
class SettingsDialog(UserInterface):
    
    def __init__(self):
        
        UserInterface.__init__(self, "settings_dialog.ui")
        
    def run(self):
        
        dlg = self.settings_dialog
        
        settings = Settings.get()
        
        self.show_line_numbers.set_active(settings.show_line_numbers)
        
        if dlg.run() == gtk.RESPONSE_OK:
            settings.show_line_numbers = self.show_line_numbers.get_active()
             
        dlg.hide()
 