/*
* This file was generated automatically.
* Please do not edit!
*/

#include "audio_playerstatus.h"

GType audio_playerstatus_get_type() {

    static GType enum_type = 0;
    GEnumValue* values;
    guint idx;
    
    if (!enum_type) {
    
        values = g_new(GEnumValue, 3+1);
        idx = 0;

        values[idx].value = AUDIO_PLAYER_STATUS_READY;
        values[idx].value_name = "READY";
        values[idx].value_nick = "READY";
        idx++;

        values[idx].value = AUDIO_PLAYER_STATUS_PLAYING;
        values[idx].value_name = "PLAYING";
        values[idx].value_nick = "PLAYING";
        idx++;

        values[idx].value = AUDIO_PLAYER_STATUS_PAUSED;
        values[idx].value_name = "PAUSED";
        values[idx].value_nick = "PAUSED";
        idx++;

        values[idx].value = 0;
        values[idx].value_name = NULL;
        values[idx].value_nick = NULL;
    
        enum_type = g_enum_register_static("AudioPlayerStatus", values);
        
    }

    return enum_type;
    
}

