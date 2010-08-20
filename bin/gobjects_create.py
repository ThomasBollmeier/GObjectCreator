#!/usr/bin/python
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

from optparse import OptionParser

import gobject_creator
from gobject_creator.io.py_input import read_metadata_from_py_def_files
from gobject_creator.code_generation.generation_inout import GenInputDir, GenOutputDir
import gobject_creator.code_generation.gobject.generator_gobject as gobject
import gobject_creator.code_generation.vala.generator_vala as vala
import gobject_creator.code_generation.csharp.generator_csharp as csharp

class Language:
    
    GOBJECT = "GObject"
    VALA = "Vala"
    CSHARP = "C#"
    
    @staticmethod
    def get_all():
        
        return (Language.GOBJECT, 
                Language.VALA, 
                Language.CSHARP)
        
def _create_option_parser():
    
    res = OptionParser(usage = "usage: %prog [options] <definition_file> [<def_file2> ...]", 
                       version = "%%prog, Version: %s, Author: Thomas Bollmeier" % \
                                 gobject_creator.VERSION
                       )
    
    res.add_option("-d", "--dir",
                   dest = "dest_dir",
                   default = "",
                   metavar = "DIR",
                   help = "generate files in directory DIR"
                   )

    res.add_option("-s", "--source-dir",
                   dest = "source_dir",
                   default = "",
                   metavar = "DIR",
                   help = "lookup previous versions of generated files in directory DIR"
                   )

    res.add_option("-r", "--root",
                   dest = "obj_name",
                   default = "",
                   metavar = "OBJ_NAME",
                   help = "generate object OBJ_NAME only"
                   )
        
    languages = ""
    for lang in Language.get_all():
        if languages:
            languages += ", "
        languages += lang
        
    help_str = "generate in language LANGUAGE (values: %s, default: %s)" % \
        (languages, Language.GOBJECT)
        
    res.add_option("-l", "--language",
                   dest = "language",
                   default = Language.GOBJECT,
                   metavar = "LANGUAGE",
                   help = help_str
                   )

    res.add_option("-I", "--include",
                   action = "append",
                   dest = "paths",
                   default = [],
                   metavar = "DIR",
                   help = "add DIR to search path for definition files"
                   )
    
    res.add_option("-v",
                   action = "store_true",
                   dest = "verbose",
                   help = "write generation info to standard output"
                   )
    
    res.add_option("", "--header-comment",
                   dest = "header_comment_file",
                   default = "",
                   metavar = "FILE",
                   help = "add header comment from FILE to generated code"
                   )
            
    return res
    
# ===== MAIN =====

# parse options:

parser = _create_option_parser()

options, def_files = parser.parse_args()

if options.language not in Language.get_all():
    print "Error: Unknown language '%s'!" % options.language
    exit(1)
  
if len(def_files) == 0:
    parser.print_help()
    exit(1)
    
packages, classes, interfaces, error_domains, enums = \
    read_metadata_from_py_def_files(def_files, options.paths, options.obj_name)
    
if options.language == Language.GOBJECT:
    generator = gobject.Generator(options.header_comment_file)
elif options.language == Language.VALA:
    generator = vala.Generator()
elif options.language == Language.CSHARP:
    generator = csharp.Generator()

if not options.dest_dir:
    if not options.source_dir:
        options.source_dir = "."
    options.dest_dir = options.source_dir
else:
    if not options.source_dir:
        options.source_dir = options.dest_dir

generation_input = GenInputDir(options.source_dir)
generation_output = GenOutputDir(options.dest_dir, inVerbose=options.verbose)

for pack in packages:
    generator.createPackage(pack, generation_input, generation_output)
    
for cls in classes:
    generator.createClass(cls, generation_input, generation_output)
    
for intf in interfaces:
    generator.createInterface(intf, generation_input, generation_output)
    
for error_domain in error_domains:
    generator.createErrorDomain(error_domain, generation_input, generation_output)

for enum in enums:
    generator.createEnumeration(enum, generation_output)
