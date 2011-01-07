# coding=UTF-8

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

class ObjectCatalog(object):
    
    __single = None
    
    @staticmethod
    def get():
        
        if not ObjectCatalog.__single:
            ObjectCatalog.__single = ObjectCatalog()
            
        return ObjectCatalog.__single
    
    def __init__(self):
        
        self._top_objects = {}
    
    def add_top_object(self, in_top_object):
        
        try:
            if in_top_object.parent:
                raise NoTopObjectError
        except AttributeError:
            pass
        
        if in_top_object.name in self._top_objects:
            raise ObjectExistsError(in_top_object.name)
        
        self._top_objects[in_top_object.name] = in_top_object
        
    def get_top_objects(self):
        
        return self._top_objects
    
    def get_object(self, in_obj_name):
        
        names = in_obj_name.split(".")
        
        try:
            result = self._top_objects[names[0]]
        except KeyError:
            raise ObjectNotFoundError(names[0])
        
        for name in names[1:]:
            try:
                result = getattr(result, name)
            except AttributeError:
                raise ObjectNotFoundError(name)
            
        return result
        
class NoTopObjectError(Exception):
    
    pass
        
class ObjectExistsError(Exception):
    
    def __init__(self, in_name):
        
        self._name = in_name
        
    def __str__(self):
        
        return "Object does not exist: %s" % self._name
    
class ObjectNotFoundError(Exception):
    
    def __init__(self, in_name):
        
        self._name = in_name
        
    def __str__(self):
        
        return "Object not found: %s" % self._name