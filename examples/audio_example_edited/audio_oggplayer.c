/*
* This file was generated automatically.
* Please edit user code sections only!
*/

#include "audio_oggplayer.h"

/* UserCode source_top { */
/* add further definitions...*/
#include "audio_playerstatus.h"
/* } UserCode */

struct _AudioOggPlayerPrivate {
	AudioPlayerStatus status;
	gchar* current;
};

/* ===== Private Methods (Declaration) ===== */

void audio_oggplay_start_im(AudioIPlayer* object, 
	const gchar* track_uri, 
	AudioFormat format, 
	GError** error
	);
gboolean audio_oggplay_stop_im(AudioIPlayer* object);
gboolean audio_oggplay_pause_im(AudioIPlayer* object);

/* UserCode further_methods { */
	/* define further methods... */
/* } UserCode */

/* ===== Properties ===== */

enum {
	PROP_STATUS = 1
};

void audio_oggplay_set_property(
	GObject* in_object,
	guint in_property_id,
	const GValue* in_value,
	GParamSpec* in_param_spec
	);
	 
void audio_oggplay_get_property(
	GObject* in_object,
	guint in_property_id,
	GValue* in_value,
	GParamSpec* in_param_spec
	);
	
/* ===== Class-Initialization ===== */

void audio_oggplay_class_init(AudioOggPlayerClass* in_class) {

	GObjectClass* gobj_class = G_OBJECT_CLASS(in_class);
	GParamSpec* pspec_status;

/* UserCode class_init { */
	/* init class members...*/
/* } UserCode */
	
	gobj_class->dispose = audio_oggplay_dispose;
	gobj_class->finalize = audio_oggplay_finalize;
	gobj_class->set_property = audio_oggplay_set_property;
	gobj_class->get_property = audio_oggplay_get_property;
	
	/* set default implementations of virtual methods */

	/* set implementations for redefined methods */

	/* add properties... */
/* UserCode property_reg_status { */
	pspec_status = g_param_spec_enum(
		"status",
		"player's status",
		"player's status",
		AUDIO_TYPE_PLAYERSTATUS,
		AUDIO_PLAYER_STATUS_READY,
		G_PARAM_READABLE|G_PARAM_STATIC_STRINGS
		);
		
	g_object_class_install_property(
		gobj_class,
		PROP_STATUS,
		pspec_status
		);

/* } UserCode */
	
}

void audio_oggplay_audio_iplayer_init(AudioIPlayerIface* in_iface) {
	
	in_iface->pause = audio_oggplay_pause_im;
	in_iface->start = audio_oggplay_start_im;
	in_iface->stop = audio_oggplay_stop_im;

}

/* UserCode external_interfaces_init { */
/* Initialize implementation of unmodeled interfaces... */
/* } UserCode */

/* ===== Type Registration ===== */

void audio_oggplay_instance_init(
	GTypeInstance* in_object,
        gpointer in_class
	) {

	AudioOggPlayer* self = (AudioOggPlayer*) in_object;
	/* Initialize members. 
	Init method of super classes are called automatically.
	*/
	self->priv = (AudioOggPlayerPrivate*) g_new(AudioOggPlayerPrivate, 1);
/* UserCode instance_init { */
	self->priv->status = AUDIO_PLAYER_STATUS_READY;
	self->priv->current = NULL;
/* } UserCode */
	
}

GType audio_oggplay_get_type() {

	static GType audio_oggplay_type = 0;
	
	if (!audio_oggplay_type) {
	
		const GTypeInfo audio_oggplay_info = {
			sizeof(AudioOggPlayerClass),
			NULL, /* base initializer */
			NULL, /* base finalizer */
			(GClassInitFunc) audio_oggplay_class_init,
			NULL, /* class finalizer */
			NULL, /* class data */
			sizeof(AudioOggPlayer),
			0, 
			audio_oggplay_instance_init
			};
			
		const GInterfaceInfo audio_iplayer_info = {
			(GInterfaceInitFunc) audio_oggplay_audio_iplayer_init,
			NULL,
			NULL
			};

		audio_oggplay_type = g_type_register_static(
			G_TYPE_OBJECT,
			"AudioOggPlayer",
			&audio_oggplay_info,
			0
			);
			
		g_type_add_interface_static(
			audio_oggplay_type,
			AUDIO_TYPE_IPLAYER,
			&audio_iplayer_info
			);

/* UserCode external_interfaces_register { */
		/* Register implementation of unmodeled interfaces... */
/* } UserCode */
	}
	
	return audio_oggplay_type;
}

/* ===== Implementation ===== */

void audio_oggplay_init(AudioOggPlayer* self) {

/* UserCode constructor { */
	/* init your members */
/* } UserCode */
	
}

/**
* audio_oggplay_new:
*
* Return value: (full):
*
*/
AudioOggPlayer* audio_oggplay_new() {

	AudioOggPlayer* result = g_object_new(AUDIO_TYPE_OGGPLAYER, NULL);

	audio_oggplay_init(result);

	return result;
}

void audio_oggplay_dispose(GObject* in_object) {

/* UserCode dispose { */
	/* unref... */
/* } UserCode */

}

void audio_oggplay_finalize(GObject* in_object) {

	AudioOggPlayer* self = AUDIO_OGGPLAYER(in_object);

/* UserCode destructor { */
	/* free allocated memory ...*/
	if (self->priv->current)
		g_free(self->priv->current);
/* } UserCode */

	g_free(self->priv);

}

void audio_oggplay_set_property(
	GObject* in_object,
	guint in_property_id,
	const GValue* in_value,
	GParamSpec* in_param_spec
	) {
	
/* UserCode property_set_data_decls { */
	/* data declarations... */
/* } UserCode */

	switch(in_property_id) {
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(
			in_object, in_property_id, in_param_spec );
		break;
	}
	
}
	 
void audio_oggplay_get_property(
	GObject* in_object,
	guint in_property_id,
	GValue* in_value,
	GParamSpec* in_param_spec
	) {

	AudioOggPlayer* self = AUDIO_OGGPLAYER(in_object);
/* UserCode property_get_data_decls { */
	/* data declarations... */
/* } UserCode */

	switch(in_property_id) {
	case PROP_STATUS:
/* UserCode property_get_status { */
		g_value_set_enum(in_value, self->priv->status);
/* } UserCode */
		break;
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(
			in_object, in_property_id, in_param_spec );
		break;
	}	
	
}

/* ===== Methods ===== */

void audio_oggplay_start_im(AudioIPlayer* object, 
	const gchar* track_uri, 
	AudioFormat format, 
	GError** error
	) {
/* UserCode start { */

	AudioOggPlayer* self = AUDIO_OGGPLAYER(object);
	gboolean resumed;

	if (self->priv->status == AUDIO_PLAYER_STATUS_PLAYING) {

		if (error) {
			*error = g_error_new(
					AUDIO_ERROR,
					AUDIO_ERROR_INVALID_STATUS,
					"Cannot start '%s': Player is playing already",
					track_uri
					);
		}

		return;
	}
	else if (format != AUDIO_FORMAT_OGG_VORBIS) {

		if (error) {
			*error = g_error_new(
					AUDIO_ERROR,
					AUDIO_ERROR_UNKNOWN_FORMAT,
					"Audio format of '%s' is not supported",
					track_uri
					);
		}

		return;
	}

	resumed = self->priv->status == AUDIO_PLAYER_STATUS_PAUSED ? 
		TRUE : FALSE; 

	self->priv->status = AUDIO_PLAYER_STATUS_PLAYING;
	
	if (self->priv->current)
		g_free(self->priv->current);
	self->priv->current = g_strdup(track_uri);

	g_signal_emit_by_name(AUDIO_IPLAYER(self), 
		"started", 
		self->priv->current, 
		resumed
		);
	
/* } UserCode */
}
gboolean audio_oggplay_stop_im(AudioIPlayer* object) {
/* UserCode stop { */

	AudioOggPlayer* self = AUDIO_OGGPLAYER(object);

	switch (self->priv->status) {
		case AUDIO_PLAYER_STATUS_PLAYING:
		case AUDIO_PLAYER_STATUS_PAUSED:
			self->priv->status = AUDIO_PLAYER_STATUS_READY;
			g_signal_emit_by_name(AUDIO_IPLAYER(self), 
				"stopped", 
				self->priv->current
				); 
			g_free(self->priv->current);
			self->priv->current = NULL;
			return TRUE;
		default:
			return FALSE;
	}
	
/* } UserCode */
}
gboolean audio_oggplay_pause_im(AudioIPlayer* object) {
/* UserCode pause { */
	
	AudioOggPlayer* self = AUDIO_OGGPLAYER(object);	

	switch (self->priv->status) {
		case AUDIO_PLAYER_STATUS_PLAYING:
			self->priv->status = AUDIO_PLAYER_STATUS_PAUSED;
			g_signal_emit_by_name(AUDIO_IPLAYER(self), 
				"paused", 
				self->priv->current
				); 
			return TRUE;
		case AUDIO_PLAYER_STATUS_PAUSED:
			self->priv->status = AUDIO_PLAYER_STATUS_PLAYING;
			g_signal_emit_by_name(AUDIO_IPLAYER(self), 
				"started", 
				self->priv->current,
				TRUE
				); 
			return TRUE;
		default:
			return FALSE;
	}

/* } UserCode */
}

/* UserCode source_bottom { */
/* insert code here ... */
/* } UserCode */
