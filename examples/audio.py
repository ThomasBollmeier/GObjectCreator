"""
Sample meta definition.
To (re)generate files enter: gobjects_create.py [-d <gendir>] audio.py
"""

with Package("Audio"):
    
    with ErrorDomain("Error"):
        
        ErrorCode("URI_NOT_FOUND")
        ErrorCode("UNKNOWN_FORMAT")

    with Enumeration("Format"):
    
        EnumCode("MP3")
        EnumCode("OGG")

    with Interface("Player"):
    
        with IntfMethod("start"):
            Param("track_uri", "const gchar*")
            Param("format", Audio.Format)
            Param("error", "GError**")    
        
        with IntfMethod("stop"):
            Result("gboolean")
        
        with IntfMethod("pause"):
            Result("gboolean")
            
    with Class("MyPlayer"):
        
        Implements(Audio.Player)
        
        with Signal("started"):
            Param("track_uri", "const gchar*")
            
        with Signal("stopped"):
            Param("track_uri", "const gchar*")
            
        with Signal("paused"):
            Param("track_uri", "const gchar*")
        