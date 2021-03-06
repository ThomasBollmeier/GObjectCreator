"""
Sample meta definition.
To (re)generate files enter: ./generate_audio_example.sh
"""

with Package("Audio"):
    
    with ErrorDomain("Error"):
        
        ErrorCode("INVALID_STATUS")
        ErrorCode("URI_NOT_FOUND")
        ErrorCode("UNKNOWN_FORMAT")

    with Enumeration("Format"):
    
        EnumCode("MP3")
        EnumCode("OGG_VORBIS")
        
    with Enumeration("PlayerStatus"):
        
        EnumCode("READY")
        EnumCode("PLAYING")
        EnumCode("PAUSED")
        
    with Interface("IPlayer"):
    
        with IntfMethod("start"):
            Param("track_uri", "const gchar*")
            Param("format", Audio.Format)
            Param("error", "GError**")    
        
        with IntfMethod("stop"):
            Result("gboolean")
        
        with IntfMethod("pause"):
            Result("gboolean")

        with Signal("started"):
            Param("track_uri", "const gchar*")
            Param("resumed", "gboolean")
            
        with Signal("stopped"):
            Param("track_uri", "const gchar*")
            
        with Signal("paused"):
            Param("track_uri", "const gchar*")
            
    with Class("OggPlayer", inAlias="oggplay"):
        
        Implements(Audio.IPlayer)
        
        Property("status",
                 "player's status", 
                 inType = PROP_ENUM,
                 inGObjectType = Audio.PlayerStatus,
                 inDefault = Audio.PlayerStatus.READY,         
                 inAccess=PROP_ACCESS_READ
                 )
            
        Attr("status", Audio.PlayerStatus)
        Attr("current", "gchar*")
        
