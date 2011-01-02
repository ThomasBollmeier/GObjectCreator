import os
import sys

_root_dir = os.path.dirname(__file__)
if _root_dir not in sys.path:
    sys.path = [_root_dir] + sys.path

VERSION="1.1.9"
