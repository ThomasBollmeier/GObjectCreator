import os
import sys
from datetime import datetime

_root_dir = os.path.dirname(__file__)
if _root_dir not in sys.path:
    sys.path = [_root_dir] + sys.path

tstmp = datetime.now()

VERSION="0.9.25-%02d%02d%04d%02d%02d%02d" \
        (tstmp.day, tstmp.month, tstmp.year,
         tstmp.hour, tstmp.minute, tstmp.second)

