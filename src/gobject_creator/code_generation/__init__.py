import os
import gobject_creator.config as config

class Target:
    
    GOBJECT = 1
    VALA = 2
    CSHARP = 3

def get_template_path(gentarget, template_name):
    
    root = config._TEMPLATE_ROOT

    if gentarget == Target.GOBJECT:
        
        path = root + os.sep + "gobject"
    
    elif gentarget == Target.VALA:
        
        path = root + os.sep + "vala"
    
    elif gentarget == Target.CSHARP:
        
        path = root + os.sep + "csharp"
    
    else:
        
        return ""
        
    path += os.sep + template_name
    path = os.path.abspath(path)

    return path
