
#ifndef __audio_iplayer_MARSHAL_H__
#define __audio_iplayer_MARSHAL_H__

#include	<glib-object.h>

G_BEGIN_DECLS

/* VOID:STRING,BOOLEAN (/dev/stdin:1) */
extern void audio_iplayer_VOID__STRING_BOOLEAN (GClosure     *closure,
GValue       *return_value,
guint         n_param_values,
const GValue *param_values,
gpointer      invocation_hint,
gpointer      marshal_data);

/* VOID:STRING (/dev/stdin:2) */
#define audio_iplayer_VOID__STRING	g_cclosure_marshal_VOID__STRING

/* VOID:STRING (/dev/stdin:3) */

G_END_DECLS

#endif /* __audio_iplayer_MARSHAL_H__ */

