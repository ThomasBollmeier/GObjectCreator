/*
* This file was generated automatically.
* Please do not edit!
*/

#ifndef AUDIO_FORMAT_H
#define AUDIO_FORMAT_H

#include "glib-object.h"

G_BEGIN_DECLS

typedef enum _AudioFormat {
    AUDIO_FORMAT_MP3,
    AUDIO_FORMAT_OGG_VORBIS
} AudioFormat;

GType audio_format_get_type();

#define AUDIO_TYPE_FORMAT audio_format_get_type()

G_END_DECLS

#endif
