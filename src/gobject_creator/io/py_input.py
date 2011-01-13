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

from .include_handling import PreProcessor
from ..metamodel.meta_objects import *
from ..metamodel.object_catalog import ObjectCatalog
from ..metamodel.introspection_info import *
from ..metamodel.introspection_decorators import *

def read_metadata_from_py_def_files(in_def_files,
                                    in_search_paths,
                                    in_root_object_name = ""
                                    ):
    
    out_packages = []
    out_classes = []
    out_interfaces = []
    out_error_domains = []
    out_enumerations = []
    
    all_def_files = _get_all_required_files(in_def_files, in_search_paths)
    
    for def_file in all_def_files:
        exec(compile(open(def_file).read(), def_file, 'exec'), globals(), ObjectCatalog.get().get_top_objects())
        
    if not in_root_object_name:
        
        objects = list(ObjectCatalog.get().get_top_objects().values())
          
        for obj in objects:
            if isinstance(obj, Package):
                if obj._package is None:
                    out_packages.append(obj)
            elif isinstance(obj, Class):
                if obj._package is None:
                    out_classes.append(obj)
            elif isinstance(obj, Interface):
                if obj._package is None:
                    out_interfaces.append(obj)
            elif isinstance(obj, ErrorDomain):
                if obj._package is None:
                    out_error_domains.append(obj)
            elif isinstance(obj, Enumeration):
                if obj._package is None:
                    out_enumerations.append(obj)
                    
    else:
        
        obj = ObjectCatalog.get().get_object(in_root_object_name)
        
        if isinstance(obj, Package):
            out_packages.append(obj)
        elif isinstance(obj, Class):
            out_classes.append(obj)
        elif isinstance(obj, Interface):
            out_interfaces.append(obj)
        elif isinstance(obj, ErrorDomain):
            out_error_domains.append(obj)
        elif isinstance(obj, Enumeration):
            out_enumerations.append(obj)
                
    return out_packages, out_classes, out_interfaces, out_error_domains, out_enumerations

def _get_all_required_files(in_def_files, in_search_paths):

    prep = PreProcessor()
    prep.add_paths(in_search_paths)
    
    result = [prep.full_name(def_file) for def_file in in_def_files]
    
    files_to_scan = result 

    while files_to_scan:
    
        new_incls = set()
    
        for f in files_to_scan:
            for incl in prep.scan_for_includes(f):
                new_incls.add(incl)
            
        files_to_scan = []
            
        for incl in new_incls:
            if incl not in result:
                result.insert(0, incl)
                files_to_scan.append(incl)
                
    return result
