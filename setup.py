from distutils.core import setup
import classmate

description = """
Generation of source files in various languages from meta definition files
"""

setup(
    name = "Classmate",
    version = classmate.VERSION,
    description = description,
    author = "Thomas Bollmeier",
    author_email = "TBollmeier@web.de",
    packages = ["classmate", 
                "classmate/code_generation",
                "classmate/code_generation/csharp",
                "classmate/code_generation/gobject",
                "classmate/code_generation/vala",
                "classmate/io",
                "classmate/metamodel"
                ],
    package_data = {"classmate" : 
                    ["code_generation/gobject/templates/*.tmpl",
                     "code_generation/vala/templates/*.tmpl",
                     "code_generation/csharp/templates/*.tmpl",
                    ]
                    },
    scripts = ["bin/classmate_gen.py"]
    )
