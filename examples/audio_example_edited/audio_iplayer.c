/*
* This file was generated automatically.
* Please edit user code sections only!
*/

#include "audio_iplayer.h"

/* UserCode source_top { */
/* Marshaller functions to be used by signals: */	
#include "audio_iplayer_marshaller.h"
/* } UserCode */

/* Signals: */

enum {
	STARTED,
	STOPPED,
	PAUSED,
	LAST_SIGNAL
};
static guint audioiplayer_signals[LAST_SIGNAL] = {0};

void audio_iplayer_base_init(AudioIPlayerIface* in_class) {

	static gboolean initialized = FALSE;
	
	if (initialized)
		return;

	/* Signal definition: */
	
/* UserCode signal_started { */

	audioiplayer_signals[STARTED] = 
		g_signal_new(
			"started",
			AUDIO_TYPE_IPLAYER,
			G_SIGNAL_RUN_LAST|G_SIGNAL_DETAILED,
			G_STRUCT_OFFSET(AudioIPlayerIface, started),
			NULL,
			NULL,
			audio_iplayer_VOID__STRING_BOOLEAN,
			G_TYPE_NONE,
			2,
			G_TYPE_STRING,
			G_TYPE_BOOLEAN
			);
		
/* } UserCode */

/* UserCode signal_stopped { */

	audioiplayer_signals[STOPPED] = 
		g_signal_new(
			"stopped",
			AUDIO_TYPE_IPLAYER,
			G_SIGNAL_RUN_LAST|G_SIGNAL_DETAILED,
			G_STRUCT_OFFSET(AudioIPlayerIface, stopped),
			NULL,
			NULL,
			audio_iplayer_VOID__STRING,
			G_TYPE_NONE,
			1,
			G_TYPE_STRING
			);
		
/* } UserCode */

/* UserCode signal_paused { */

	audioiplayer_signals[PAUSED] = 
		g_signal_new(
			"paused",
			AUDIO_TYPE_IPLAYER,
			G_SIGNAL_RUN_LAST|G_SIGNAL_DETAILED,
			G_STRUCT_OFFSET(AudioIPlayerIface, paused),
			NULL,
			NULL,
			audio_iplayer_VOID__STRING,
			G_TYPE_NONE,
			1,
			G_TYPE_STRING
			);
		
/* } UserCode */

/* UserCode interface_init { */
	/* further initializations... */
/* } UserCode */
	
	initialized = TRUE;

}  

void audio_iplayer_base_finalize(AudioIPlayerIface* in_class) {

	static gboolean finalized = FALSE;
	
	if (finalized)
		return;

/* UserCode interface_finalize { */
	/* do some final stuff... */
/* } UserCode */

	finalized = TRUE;
	
}  

GType audio_iplayer_get_type() {

	static GType audio_iplayer_type = 0;
	
	if (!audio_iplayer_type) {
	
		const GTypeInfo audio_iplayer_info = {
			sizeof(AudioIPlayerIface),
			(GBaseInitFunc) audio_iplayer_base_init,
			(GBaseFinalizeFunc) audio_iplayer_base_finalize
			};
			
		audio_iplayer_type = g_type_register_static(
			G_TYPE_INTERFACE,
			"AudioIPlayer",
			&audio_iplayer_info,
			0
			);
		
		/* all classes are allowed to implement this interface: */
		g_type_interface_add_prerequisite(audio_iplayer_type, G_TYPE_OBJECT);
		
	}
	
	return audio_iplayer_type;
}

void
audio_iplayer_start(AudioIPlayer* object, 
	const gchar* track_uri, 
	AudioFormat format, 
	GError** error
	) {

	AudioIPlayerIface* intf = AUDIO_IPLAYER_GET_INTERFACE(object);
	
	intf->start( object, track_uri, format, error);

}

gboolean
audio_iplayer_stop(AudioIPlayer* object) {

	AudioIPlayerIface* intf = AUDIO_IPLAYER_GET_INTERFACE(object);
	
	return intf->stop( object);

}

gboolean
audio_iplayer_pause(AudioIPlayer* object) {

	AudioIPlayerIface* intf = AUDIO_IPLAYER_GET_INTERFACE(object);
	
	return intf->pause( object);

}

