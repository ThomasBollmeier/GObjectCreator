/*
* This file was generated automatically.
* Please do not edit!
*/

#ifndef AUDIO_PLAYER_STATUS_H
#define AUDIO_PLAYER_STATUS_H

#include "glib-object.h"

G_BEGIN_DECLS

typedef enum _AudioPlayerStatus {
    AUDIO_PLAYER_STATUS_READY,
    AUDIO_PLAYER_STATUS_PLAYING,
    AUDIO_PLAYER_STATUS_PAUSED
} AudioPlayerStatus;

GType audio_playerstatus_get_type();

#define AUDIO_TYPE_PLAYERSTATUS audio_playerstatus_get_type()

G_END_DECLS

#endif
