from distutils.core import setup
import gobject_creator

description = "Generation of source files in various languages"
description += " from meta definition files"

setup(
    name = "GObjectCreator",
    version = gobject_creator.VERSION,
    description = description,
    author = "Thomas Bollmeier",
    author_email = "TBollmeier@web.de",
    url = "http://www.bollmeier.de/GObjectCreator",
    license = "GPLv3",
    packages = ["gobject_creator", 
                "gobject_creator/code_generation",
                "gobject_creator/code_generation/csharp",
                "gobject_creator/code_generation/gobject",
                "gobject_creator/code_generation/vala",
                "gobject_creator/io",
                "gobject_creator/metamodel",
                "gobject_creator/ui",
                "gobject_creator/ui/resources",
                ],
    package_data = {"gobject_creator" : 
                    ["code_generation/gobject/templates/*.tmpl",
                     "code_generation/vala/templates/*.tmpl",
                     "code_generation/csharp/templates/*.tmpl",
                     "ui/locale/de/LC_MESSAGES/*",
                     "ui/resources/*.ui",
                     "ui/resources/*.png",
                     "ui/resources/*.xml",
                     "ui/resources/*.lang",
                    ]
                    },
    scripts = ["bin/gobjects_create.py",
               "bin/goceditor.py"
               ]
    )
