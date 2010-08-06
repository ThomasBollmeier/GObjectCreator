/*
* This file was generated automatically.
* Please edit user code sections only!
*/

#ifndef AUDIOIPLAYER_H
#define AUDIOIPLAYER_H 

#include "glib-object.h"

G_BEGIN_DECLS

#include "audio_format.h"

/* UserCode header_top { */
#include "audio_error.h"
/* } UserCode */

/* ===== Instance ===== */

typedef struct _AudioIPlayer AudioIPlayer;

/* ===== Interface ===== */

typedef struct _AudioIPlayerIface {

	GTypeInterface base_interface;
	
	/* Methods: */
	
	gboolean (*pause)(AudioIPlayer* object);
	
	void (*start)(AudioIPlayer* object, 
	const gchar* track_uri, 
	AudioFormat format, 
	GError** error
	);
	
	gboolean (*stop)(AudioIPlayer* object);
	
	/* Signals: */

	void (*paused)(AudioIPlayer* object, 
	const gchar* track_uri
	);

	void (*started)(AudioIPlayer* object, 
	const gchar* track_uri, 
	gboolean resumed
	);

	void (*stopped)(AudioIPlayer* object, 
	const gchar* track_uri
	);

} AudioIPlayerIface;

GType audio_iplayer_get_type();

void
audio_iplayer_start(AudioIPlayer* object, 
	const gchar* track_uri, 
	AudioFormat format, 
	GError** error
	);

gboolean
audio_iplayer_stop(AudioIPlayer* object);

gboolean
audio_iplayer_pause(AudioIPlayer* object);

/* ===== Macros ===== */

#define AUDIO_TYPE_IPLAYER \
	(audio_iplayer_get_type())
#define AUDIO_IPLAYER(obj) \
	(G_TYPE_CHECK_INSTANCE_CAST((obj), AUDIO_TYPE_IPLAYER, AudioIPlayer))
#define AUDIO_IPLAYER_CLASS(cls) \
	(G_TYPE_CHECK_CLASS_CAST((cls), AUDIO_TYPE_IPLAYER, AudioIPlayerIface))
#define AUDIO_IS_IPLAYER(obj) \
	(G_TYPE_CHECK_INSTANCE_TYPE((obj), AUDIO_TYPE_IPLAYER))
#define AUDIO_IPLAYER_GET_CLASS(obj) \
	(G_TYPE_INSTANCE_GET_INTERFACE((obj), AUDIO_TYPE_IPLAYER, AudioIPlayerIface))
#define AUDIO_IPLAYER_GET_INTERFACE(obj) \
	(G_TYPE_INSTANCE_GET_INTERFACE((obj), AUDIO_TYPE_IPLAYER, AudioIPlayerIface))

G_END_DECLS

#endif
