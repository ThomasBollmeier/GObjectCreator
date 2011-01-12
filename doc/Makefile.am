EXTRA_DIST = Doxyfile

install-html-local:
	doxygen
	mkdir -p $(htmldir)
	mv -f html/* $(htmldir)
	rm -rf html

