/*
* This file was generated automatically.
* Please do not edit!
*/

#include "audio_format.h"

GType audio_format_get_type() {

    static GType enum_type = 0;
    GEnumValue* values;
    guint idx;
    
    if (!enum_type) {
    
        values = g_new(GEnumValue, 2+1);
        idx = 0;

        values[idx].value = AUDIO_FORMAT_MP3;
        values[idx].value_name = "MP3";
        values[idx].value_nick = "MP3";
        idx++;

        values[idx].value = AUDIO_FORMAT_OGG_VORBIS;
        values[idx].value_name = "OGG_VORBIS";
        values[idx].value_nick = "OGG_VORBIS";
        idx++;

        values[idx].value = 0;
        values[idx].value_name = NULL;
        values[idx].value_nick = NULL;
    
        enum_type = g_enum_register_static("AudioFormat", values);
        
    }

    return enum_type;
    
}

