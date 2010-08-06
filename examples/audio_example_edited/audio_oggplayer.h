/*
* This file was generated automatically.
* Please edit user code sections only!
*/

#ifndef AUDIOOGGPLAYER_H
#define AUDIOOGGPLAYER_H

#include "glib-object.h"

G_BEGIN_DECLS

#include "audio_iplayer.h"

/* UserCode header_top { */
/* insert code here ... */
/* } UserCode */

/* ===== Instance ===== */

typedef struct _AudioOggPlayerPrivate AudioOggPlayerPrivate;

typedef struct _AudioOggPlayer {

	GObject super;
/* UserCode properties { */
	/* add properties here... */
/* } UserCode */
	AudioOggPlayerPrivate* priv;
} AudioOggPlayer;

/* ===== Properties =====

    "status" : player's status (read)

*/

/* ===== Class ===== */

typedef struct _AudioOggPlayerClass {

	GObjectClass super_class;
	/* attributes: */
	/* virtual methods */

} AudioOggPlayerClass;

GType audio_oggplay_get_type();

AudioOggPlayer* audio_oggplay_new(
	); /* Constructor */

void audio_oggplay_init(AudioOggPlayer* self); /* to be called by derived classes */
void audio_oggplay_dispose(GObject* in_object); 
void audio_oggplay_finalize(GObject* in_object);

/* public methods: */

/* ===== Macros ===== */

#define AUDIO_TYPE_OGGPLAYER \
	(audio_oggplay_get_type())
#define AUDIO_OGGPLAYER(obj) \
	(G_TYPE_CHECK_INSTANCE_CAST((obj), AUDIO_TYPE_OGGPLAYER, AudioOggPlayer))
#define AUDIO_OGGPLAYER_CLASS(cls) \
	(G_TYPE_CHECK_CLASS_CAST((cls), AUDIO_TYPE_OGGPLAYER, AudioOggPlayerClass))
#define AUDIO_IS_OGGPLAYER(obj) \
	(G_TYPE_CHECK_INSTANCE_TYPE((obj), AUDIO_TYPE_OGGPLAYER))
#define AUDIO_IS_OGGPLAYER_CLASS(cls) \
	(G_TYPE_CHECK_CLASS_TYPE((cls), AUDIO_TYPE_OGGPLAYER))
#define AUDIO_OGGPLAYER_GET_CLASS(obj) \
	(G_TYPE_INSTANCE_GET_CLASS((obj), AUDIO_TYPE_OGGPLAYER, AudioOggPlayerClass))

/* UserCode header_bottom { */
/* insert code here ... */
/* } UserCode */

G_END_DECLS

#endif
