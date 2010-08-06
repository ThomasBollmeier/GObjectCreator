CFLAGS=`pkg-config gobject-2.0 --cflags`
LIBS=`pkg-config gobject-2.0 --libs`

OBJ_FILES=\
audio_error.o \
audio_format.o \
audio_iplayer.o \
audio_iplayer_marshaller.o \
audio_oggplayer.o \
audio_playerstatus.o \
demo.o

audio_error.o: audio_error.c
	gcc -c $(CFLAGS) audio_error.c	

audio_format.o: audio_format.c
	gcc -c $(CFLAGS) audio_format.c	

audio_iplayer.o: audio_iplayer.c
	gcc -c $(CFLAGS) audio_iplayer.c

audio_iplayer_marshaller.o: audio_iplayer_marshaller.c
	gcc -c $(CFLAGS) audio_iplayer_marshaller.c	
	
audio_oggplayer.o: audio_oggplayer.c
	gcc -c $(CFLAGS) audio_oggplayer.c	

audio_playerstatus.o: audio_playerstatus.c
	gcc -c $(CFLAGS) audio_playerstatus.c	

demo.o: demo.c
	gcc -c $(CFLAGS) demo.c	

demo: $(OBJ_FILES)
	gcc -o demo $(LIBS) $(OBJ_FILES) 

clean:
	rm -f *.o
	rm -f demo

	
