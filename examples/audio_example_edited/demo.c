#include "audio_oggplayer.h"

void on_started(
	AudioIPlayer* object, 
	const gchar* track_uri, 
	gboolean resumed,
	gpointer user_data
	);

void on_stopped(
	AudioIPlayer* object, 
	const gchar* track_uri,
	gpointer user_data
	);
 
void on_paused(
	AudioIPlayer* object, 
	const gchar* track_uri,
	gpointer user_data
	);

void log_error(GError** error);

int main() {

	AudioIPlayer* player;
	gchar* stream_info = "Deutschlandradio Kultur";
	GError* error = NULL;

	g_type_init();

	player = AUDIO_IPLAYER(audio_oggplay_new());

	g_signal_connect(player, 
                "started",
                G_CALLBACK(on_started),
                stream_info
                );
	g_signal_connect(player, 
                "stopped",
                G_CALLBACK(on_stopped),
                stream_info
                );
	g_signal_connect(player, 
                "paused",
                G_CALLBACK(on_paused),
                stream_info
                );

	audio_iplayer_start(player, 
                "bird_of_paradise.ogg",
                AUDIO_FORMAT_OGG_VORBIS,
                &error
                );

        if (error)
		log_error(&error);

	audio_iplayer_start(player, 
                "relaxin_at_camarillo.ogg",
                AUDIO_FORMAT_OGG_VORBIS,
                &error
                );

        if (error)
		log_error(&error);

	audio_iplayer_pause(player);

	audio_iplayer_pause(player);

	audio_iplayer_stop(player);	

	audio_iplayer_start(player, 
                "moondreams.mp3",
                AUDIO_FORMAT_MP3,
                &error
                );

        if (error)
		log_error(&error);

        g_object_unref(player);

        return 0;

}

void on_started(
	AudioIPlayer* object, 
	const gchar* track_uri, 
	gboolean resumed,
	gpointer user_data
	) {

	gchar* stream_info = (gchar*) user_data;

	if (!resumed)
		g_print("(%s) Now playing: %s\n", stream_info, track_uri);
	else
		g_print("(%s) Resuming: %s\n", stream_info, track_uri);

}

void on_stopped(
	AudioIPlayer* object, 
	const gchar* track_uri,
	gpointer user_data
	) {

	gchar* stream_info = (gchar*) user_data;

	g_print("(%s) Stopped: %s\n", stream_info, track_uri);

}
 
void on_paused(
	AudioIPlayer* object, 
	const gchar* track_uri,
	gpointer user_data
	) {

	gchar* stream_info = (gchar*) user_data;

	g_print("(%s) Paused: %s\n", stream_info, track_uri);

}

void log_error(GError** error) {

        g_printerr("%s\n", (*error)->message);
        g_error_free(*error);
        *error = NULL;

}
